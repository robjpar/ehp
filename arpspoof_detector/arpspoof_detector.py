import scapy.all as sc


def get_mac(ip):
    arp_request = sc.ARP(pdst=ip)
    broadcast = sc.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = sc.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def process_sniffed_packet(packet):
    if packet.haslayer(sc.ARP) and packet[sc.ARP].op == 2:
        try:
            real_mac = get_mac(packet[sc.ARP].psrc)
            response_mac = packet[sc.ARP].hwsrc
            if real_mac != response_mac:
                print('[+] You are under attack!')
        except IndexError:
            pass

def sniff(interface):
    sc.sniff(iface=interface, store=False, prn=process_sniffed_packet)


sniff('eth0')
