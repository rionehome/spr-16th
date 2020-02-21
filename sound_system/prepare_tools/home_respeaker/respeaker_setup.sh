#!/bin/sh
echo "--------caution---------"
echo "do you connect re-speaker?(y/n)"
read respeaker
if [ $respeaker = 'y' ]; then
    echo "install pyusb click?(y/n)"
    read pyusb
    echo "install usb_4_mic_array?(y/n)"
    read usb_4_mic_array
    if [ $pyusb = 'y' ]; then
        sudo apt-get update
        sudo pip install pyusb click
    fi
    if [ $usb_4_mic_array = 'y' ]; then
        cd
        git clone https://github.com/respeaker/usb_4_mic_array.git
        cd usb_4_mic_array
        sudo python dfu.py --download 6_channels_firmware.bin
    fi
    cd
    cd /etc/udev/rules.d/
    sudo touch 10-any_name_is_ok.rules 10-any_name_is_ok.rules
    echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="2886", ATTR{idProduct}=="0018", MODE="0666", GROUP="plugdev"' | sudo tee 10-any_name_is_ok.rules
    username=$(whoami)
    sudo gpasswd -a $username plugdev
    sudo chmod a+r /etc/udev/rules.d/10-any_name_is_ok.rules
    sudo udevadm control --reload-rules
    udevadm trigger

    echo 'rebooting....'
    sleep 2
    sudo reboot
fi

