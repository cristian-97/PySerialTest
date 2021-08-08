import os
import errno

#ftdi_usb_base_path = '/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.2/1-1.2:1.0/ttyUSB'
#u2d2_usb_base_path = '/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.3/1-1.3:1.0/ttyUSB'

#ftdi_usb_base_path = '/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.1/1-1.1.2/1-1.1.2:1.0/ttyUSB'
#u2d2_usb_base_path = '/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.1/1-1.1.3/1-1.1.3:1.0/ttyUSB'

# il valore vicino le porte indica il parametro da passare a usb_path_finder
#  |-----------------------------------------|
#  ||----   ----|[1.2] Phaser2 | [1.4] rfid||
#  || ethernet  |----------------------------|
#  ||           |[1.1] Phaser1 |[1.3] Target||
#  |-----------------------------------------|
#


base_paths = [
    #'/sys/bus/usb/drivers/usb/1-{path}/1-{path}:1.0/ttyUSB{ttyUSB}', #pc lorenzo
    '/sys/bus/usb/drivers/usb/1-1/1-{path}/1-{path}:1.0/ttyUSB{ttyUSB}',  # pi4
    #'/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.2/1-1.2:1.0/ttyUSB',
    '/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-{path}/1-{path}:1.0/ttyUSB{ttyUSB}',           # pi2
    #'/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.1/1-1.1.2/1-1.1.2:1.0/ttyUSB',
    '/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.1/1-1.{path}/1-1.{path}:1.0/ttyUSB{ttyUSB}'  # pi3
]


class FileNotFoundError(OSError):
    pass


def find_dev_by_path(path):
    for p in base_paths:
        for i in range(0, 10):
            if os.path.exists(p.format(path=path, ttyUSB=i)):
                return '/dev/ttyUSB{ttyUSB}'.format(ttyUSB=i)

    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), '/dev/ttyUSB<?>')