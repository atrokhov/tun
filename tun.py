import os
import subprocess

tun = open('/dev/tun0', 'r+b')
subprocess.check_call('ifconfig tun0 192.168.137.1 192.168.137.10 up', shell=True)

while True:
    packet = list(os.read(tun.fileno(), 2048))

    packet[12:16], packet[16:20] = packet[16:20], packet[12:16]
    packet[20] = chr(0)
    packet[22:24] = chr(0), chr(0)
    checksum = 0

    for i in range(20, len(packet), 2):
        half_word = (ord(packet[i]) << 8) + ord(packet[i+1])
        checksum += half_word

    checksum = ~(checksum + 4) & 0xffff

    packet[22] = chr(checksum >> 8)
    packet[23] = chr(checksum & ((1 << 8) - 1))

    os.write(tun.fileno(), ''.join(packet))