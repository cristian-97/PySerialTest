import serial
import struct
import time
import ctypes
import color
import traceback

'''Registri:
id_device          
reg 1-2-3:R-G-B ---------------- R-G-B ∈ [0;255]
reg 4:strobe/fade --------------- strobe ∈ [0;127] fade ∈ [128;255]
reg 5:infrarosso/other_effects ----- infrarosso ∈ [0;5] other_effect ∈ [0;63]
reg 6: da implementare
'''


class OpSerial:

    def __init__(self,usb_port):
        self.color = color.ColorSelector()
        self.dev_reg = {}
        self.msg_list = []
        self.t_last_send = 0
        self.terminator = struct.pack('B', 3)
        self.ser = serial.Serial(usb_port, 9600, timeout=1)
        if not self.ser.is_open:
            self.ser.open()

    def dec_to_hex(self, dec_value):
        hex_value = format(dec_value, 'X')
        if len(hex_value) == 1:
            hex_value = '0' + hex_value
        return hex_value

    def __set_ir_value(self, player_id):
        ir_list = [0, 0b01, 0b10, 0b100, 0b1000, 0b1111]
        return ir_list[player_id]

    def __op_bin(self, ir_value, effect_value):
        # ir_value:0--5  effect_value: 0--15
        ir_value = self.__set_ir_value(ir_value)
        effect_value <<= 4
        reg_value = effect_value | ir_value
        hex_reg = format(reg_value, 'X')

        if len(hex_reg) == 1:
            hex_reg = '0' + hex_reg

        return hex_reg

    def reset_msg_list(self):
        self.msg_list = [''] * (len(self.dev_reg) + 1)

    def reset_all(self):
        # invia un messaggio che fa riavviare tutti i dispositivi
        # time_send = time.time()
        # while time.time() - time_send < 3:
        send = struct.pack('B', 17)
        print(">> " + str(send))
        self.ser.write(send)
        time.sleep(1)

    def dev_init(self):
        # inizializzo tutti i dispositivi inviando al primo l'id 01
        sending = True
        time_conf = time.time()
        time_send = time.time()
        send = struct.pack('BBBB', 1, 48, 49, 3)
        print(">> " + str(send))

        while sending:
            # try:
            buff = []
            if time.time() - time_conf > 5:
                sending = False
            if time.time() - time_send > 2:
                send = struct.pack('BBBB', 1, 48, 49, 3)
                print(">> " + str(send))
                self.ser.write(send)
                time_send = time.time()
            starter = []
            if self.ser.inWaiting() > 0:
                text = self.ser.read()
                try:
                    starter = struct.unpack('B', text)
                except struct.error:
                    starter.append(False)

                if starter[0] == 1:

                    text = self.ser.read_until(self.terminator)
                    print(text)
                    text = text[0:len(text) - 1]
                    tmp = struct.unpack('BB', text)
                    buff.append(chr(tmp[0]))
                    buff.append(chr(tmp[1]))
                    tmp = ''.join(buff)
                    x = int(tmp, 16)
                    key = 'dev' + str(x)
                    print(key)
                    if key not in self.dev_reg:
                        self.dev_reg[key] = x
            # except struct.error:
            #   print(traceback.format_exc())

        return self.dev_reg

    def stop(self):
        print("session terminated!")
        self.ser.close()

    def set_register(self, target_list, color, fade_strobe, ir_value, reg5_effect):

        reg5 = self.__op_bin(ir_value, reg5_effect)
        reg4 = self.dec_to_hex(fade_strobe)
        rgb = self.color.choose_color(color)
        for target in target_list:
            if target in self.dev_reg.values():
                hex_id = self.dec_to_hex(target)
                self.msg_list[target] = struct.pack('BBBBBBBBBBBBBB', ord(hex_id[0]), ord(hex_id[1]), ord(rgb[0]),
                                                    ord(rgb[1]), ord(rgb[2]), ord(rgb[3]), ord(rgb[4]), ord(rgb[5]),
                                                    ord(reg4[0]), ord(reg4[1]), ord(reg5[0]), ord(reg5[1]), 55, 55)

    def remove_target(self, target_list):
        reg5 = self.__op_bin(0, 0)
        reg4 = self.dec_to_hex(0)
        rgb = self.color.choose_color(-1)
        for target in target_list:
            if target in self.dev_reg.values():
                hex_id = self.dec_to_hex(target)
                self.msg_list[target] = struct.pack('BBBBBBBBBBBBBB', ord(hex_id[0]), ord(hex_id[1]), ord(rgb[0]),
                                                    ord(rgb[1]), ord(rgb[2]), ord(rgb[3]), ord(rgb[4]), ord(rgb[5]),
                                                    ord(reg4[0]), ord(reg4[1]), ord(reg5[0]), ord(reg5[1]), 55, 55)

    def read_shot(self):
        try:
            id = []
            shot = []
            buff = []
            starter = []
            if self.ser.inWaiting() > 0:
                text = self.ser.read()
                starter = struct.unpack('B', text)

                if starter[0] == 2:
                    text = self.ser.read_until(self.terminator)
                    buff = struct.unpack('BBBB', text[:-1])
                    id = (chr(buff[0]),chr(buff[1]))
                    shot = (chr(buff[2]), chr(buff[3]))
                    x = int(''.join(id), 16)
                    key = 'dev%s' % x
                    x = int(''.join(shot), 16)
                    if x in [1, 2, 3, 4, 5]:
                        return key, x
        except:
            print(traceback.format_exc())
        return 0, 0

    def send_msg(self):
        msg_to_send = []
        for msg in self.msg_list:
            if len(msg) == 14:
                msg_to_send.append(msg)
                if len(msg_to_send) > 14:
                    send = b''.join([struct.pack('B', 2)] + msg_to_send + [struct.pack('B', 3)])
                    if time.time() - self.t_last_send < 0.2:
                        time.sleep(0.15)
                    self.ser.write(send)
                    self.t_last_send = time.time()
                    print(send)
                    msg_to_send = []

        if msg_to_send:
            send = b''.join([struct.pack('B', 2)] + msg_to_send + [struct.pack('B', 3)])
            if time.time() - self.t_last_send < 0.2:
                time.sleep(0.15)
            self.ser.write(send)
            self.t_last_send = time.time()
            print(send)


if __name__ == '__main__':
    ser = OpSerial()
    ser.reset_all()
    dev_reg = ser.dev_init()
    n_dev = len(dev_reg)
    ser.msg_list = [''] * (n_dev+1)
    ser.remove_target([1])
    ser.send_msg()
    time.sleep(1)
    ser.set_register(dev_reg.values(), 1, 0, 0, 0)
    ser.send_msg()

    ser.stop()
