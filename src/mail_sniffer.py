import threading
from scapy.all import *


# our packet callback
def packet_callback(packet):
    print(packet.show())


# fire up our sniffer
sniff(filter="tcp port 110 or tcp port 25 or tcp port 143 or tcp port 465 or tcp port 994", prn=packet_callback, store=0)
