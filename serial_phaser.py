import serial
import struct
import time
import ctypes
import color
import traceback

'''Registri:
id_device          
reg 1-2-3:R-G-B ∈ [0;255]
reg 4:score ∈ [0;65535]=[0;ffff]
reg 5:weapon ∈ [0;9]
reg 6: name = 21 char
'''


class OpSerial:

    def __init__(self,usb_port,id):
        self.color_selec = color.ColorSelector()
        self.msg=None
        self.t_last_send = 0
        self.id=id
        self.terminator = struct.pack('B', 3)
        self.color=0
        self.score=0
        self.weapon=0
        self.name=''
        self.ser = serial.Serial(usb_port, 115200, timeout=1)
        if not self.ser.is_open:
            self.ser.open()

    def dec_to_hex(self, dec_value):
        hex_value = format(dec_value, 'X')
        return hex_value

    def stop(self):
        print("session terminated!")
        self.ser.close()

    def enable_phaser(self, color, score,weapon,name):
        self.score=score
        self.color=color
        self.weapon=weapon
        self.name=name
        h_score = '0000'+self.dec_to_hex(score)
        rgb = self.color_selec.choose_color(color)
        self.msg = struct.pack('BBBBBBBBBBBBB21sB', 1,ord(str(self.id)),ord(rgb[0]),ord(rgb[1]), ord(rgb[2]), ord(rgb[3]),
                               ord(rgb[4]), ord(rgb[5]),ord(h_score[-4]),ord(h_score[-3]),ord(h_score[-2]),ord(h_score[-1]),
                               ord(str(weapon)),name.encode('utf-8'), 3)
        self.ser.write(self.msg)

    def disable_phaser(self):
        h_score = '0000' + self.dec_to_hex(self.score)
        rgb = self.color_selec.choose_color(self.color)
        self.msg = struct.pack('BBBBBBBBBBBBB21sB', 1, ord(str(self.id)), ord(rgb[0]), ord(rgb[1]), ord(rgb[2]), ord(rgb[3]),
                               ord(rgb[4]), ord(rgb[5]), ord(h_score[-4]), ord(h_score[-3]), ord(h_score[-2]),
                               ord(h_score[-1]),ord(str(self.weapon)), self.name.encode('utf-8'), 3)
        self.ser.write(self.msg)

    def set_score(self,score):
        self.score = score
        h_score = '0000' + self.dec_to_hex(score)
        struct.pack('BBBBBB', 2, ord(h_score[-4]), ord(h_score[-3]), ord(h_score[-2]),ord(h_score[-1]), 3)
        self.ser.write(self.msg)

    def check_init_parameter(self):
        try:
            if self.ser.inWaiting() > 0:
                text = self.ser.read()
                starter = struct.unpack('B', text)

                if starter[0] == 1:
                    text = self.ser.read_until(self.terminator)
                    print(text)
                    return b'\x01' + text == self.msg
        except:
            print(traceback.format_exc())
        return False

    def reading(self):
        while 1:
            print(self.ser.read())

if __name__=='__main__':
    import usb_path_finder
    import time
    phaser_port= usb_path_finder.find_dev_by_path('3')
    ser= OpSerial(phaser_port,1)
    ser.enable_phaser(2,0,1,'MarcociaociaoMarcociaociao')
    #ser.reading()
    time.sleep(0.1)
    while not ser.check_init_parameter():
        ser.enable_phaser(1, 0, 1, 'Marco')
        time.sleep(1)
    print('ok')