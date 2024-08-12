# Search for IR code in NEC format
# To use, set byte1 and byte2 to the correct address

import subprocess


start = "+8976 -4432"
zero_sig = " +576 -544"
one_sig = " +576 -1664"
end = " +576 -41008 +8992 -2224 +576 #"


def byte_to_binary_lsb(num):
  return f"{num:08b}"[::-1]


def build_signal(binary_str):
  signal = start
  for x in binary_str:
    if x == "0":
      signal += zero_sig
    else:
      signal += one_sig
  signal += end
  return signal


def main():
  byte1 = 128
  byte2 = 222
  for byte3 in range(0, 256):
    # byte4 byte is always inverse of byte3
    byte4 = 255 - byte3
    
    input(f"Press enter to send D={byte1},S={byte2},F={byte3}")
    
    binary_str = f"{byte_to_binary_lsb(byte1)}{byte_to_binary_lsb(byte2)}{byte_to_binary_lsb(byte3)}{byte_to_binary_lsb(byte4)}"
    signal = build_signal(binary_str)
  
    script_child = subprocess.Popen(['python3', 'tiqiaa_usb_ir.py', "-s", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    script_child.communicate(signal.encode())


if __name__ == "__main__":
    main()