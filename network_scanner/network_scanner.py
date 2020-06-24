import scapy.all as sc


def scan(ip):
    arp_request = sc.ARP(pdst=ip)
    broadcast = sc.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request

    print(arp_request.summary())
    print(broadcast.summary())
    print(arp_request_broadcast.summary())

    arp_request.show()
    broadcast.show()
    arp_request_broadcast.show()


scan('10.0.2.1/24')
