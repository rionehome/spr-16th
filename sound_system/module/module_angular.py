import module_tuning
import usb.core
import usb.util
import time

def angular():
    time.sleep(3)
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
    #print dev
    if dev:
        Mic_tuning = module_tuning.Tuning(dev)
        while True:
            try:
                print(Mic_tuning.direction)
                time.sleep(1)
                break  # 一時保存用
            except KeyboardInterrupt:
                break
    return Mic_tuning.direction

if __name__ == "__main__":
    angular()
