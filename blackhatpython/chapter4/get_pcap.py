# snifferを使って通信を監視し、pcapファイルに保存する。
import sys
from scapy.all import *

print("[*] Program started")
print("[*] Please browse the site in your browser.")

if len(sys.argv) != 5:
    print("[Err] parameter error")
    sys.exit()

_count     = int(sys.argv[1])
_ip        = sys.argv[2]
_tcp_port  = sys.argv[3]
_interface = sys.argv[4]


packets = sniff(count=_count,filter="ip host %s and tcp port %s" % (_ip, _tcp_port), iface=_interface)

wrpcap("bhp.pcap", packets)

print("[*] End")
