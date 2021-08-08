import pygame
from time import time
pygame.init()
pygame.mixer.init()
file='file.wav'
sound_stop = pygame.mixer.Sound("Effects/start.flac")
pygame.mixer.music.load(file)
pygame.mixer.music.play()
tempo= time()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
    if time() - tempo >3:
        sound_stop.play()
        tempo=time()
'''import serial
import struct
import time
import usb_path_finder

target_port = usb_path_finder.find_dev_by_path('3')

terminator = struct.pack('B', 3)
ser = serial.Serial(target_port, 115200, timeout=2)
if not ser.is_open:
    ser.open()
msg = struct.pack('BBBBBBBBBBBBB21sB', 1,ord('1'),ord('f'),ord('f'),ord('0'),ord('0'),ord('0'),ord('0'),ord('9'),ord('9')
                  ,ord('9'),ord('9'),ord('1'),b'filippo',3)
msg2= struct.pack('BBBBBB', 2,ord('0'),ord('0'),ord('0'),ord('0'),3)
#for char in msg:
print(ser.write(msg),end=' ')
    #time.sleep(0.01)
print(' ')'''



