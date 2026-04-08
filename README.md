# Tiqiaa USB IR (Python)

Based on [pawitp's Python port](https://gitlab.com/pawitp/tiqiaa-usb-ir-py), which is based on
XenRE's post at https://habr.com/ru/post/494800/ and
their code published at https://gitlab.com/XenRE/tiqiaa-usb-ir.

## Device

Tiqiaa Tview USB IR transceiver (Silicon Labs chip). Shows up in dmesg as:

```
usb 5-1: New USB device found, idVendor=10c4, idProduct=8468, bcdDevice= 0.00
usb 5-1: Product: Tview
usb 5-1: Manufacturer: Tiqiaa
```

There is no Linux kernel driver for this device — `usbhid` rejects it because it uses
vendor-specific bulk endpoints instead of standard HID interrupt endpoints. This tool
talks to it directly via libusb/pyusb.

Note: some cheap clones are TX-only (no IR receiver). If `-r` hangs without
capturing anything, your dongle likely lacks a receiver.

## Setup

```bash
pip install pyusb
```

Udev rule for non-root access:

```bash
sudo tee /etc/udev/rules.d/99-tiqiaa.rules <<< 'SUBSYSTEM=="usb", ATTR{idVendor}=="10c4", ATTR{idProduct}=="8468", MODE="0666"'
sudo udevadm control --reload-rules && sudo udevadm trigger
```

## Usage

Send an IR signal:

```bash
python3 tiqiaa_usb_ir.py -s ir/cool_on_21.ir
```

Receive/capture IR signals (if your dongle has a receiver):

```bash
python3 tiqiaa_usb_ir.py -r
```

## Included IR signals

Pre-built signals for Mitsubishi Heavy Industries AC (remote RLA502A704A):

| File | Description |
|------|-------------|
| `ir/cool_on_24.ir` | Cool on, 24°C, fan auto |
| `ir/cool_on_21.ir` | Cool on, 21°C, fan auto |
| `ir/off.ir` | Power off |
