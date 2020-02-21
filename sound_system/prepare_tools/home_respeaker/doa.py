from tuning import Tuning
import usb.core
import usb.util
import time
import socket

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#print dev
if dev:
    Mic_tuning = Tuning(dev)
    while True:
        try:
            print Mic_tuning.direction
            s.sendto(str(Mic_tuning.direction),('127.0.0.1',50007))
            time.sleep(1)
        except KeyboardInterrupt:
            break

