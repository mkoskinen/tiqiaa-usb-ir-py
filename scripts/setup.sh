#!/bin/bash
set -e

echo "Installing dependencies..."
sudo dnf install -y libusb1

pip3 install pyusb

echo "Setting up udev rule for non-root access..."
sudo tee /etc/udev/rules.d/99-tiqiaa.rules <<< 'SUBSYSTEM=="usb", ATTR{idVendor}=="10c4", ATTR{idProduct}=="8468", MODE="0666"'
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "Done. Plug in the Tiqiaa USB IR dongle and you're good to go."
