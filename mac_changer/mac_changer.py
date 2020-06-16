import subprocess
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', dest='interface',
                        help='interface to change its MAC address')
    parser.add_argument('-m', '--mac', dest='new_mac', help='new MAC address')
    args = parser.parse_args()
    if not args.interface:
        parser.error(
            '[-] Please specify an interface, use --help for more info')
    if not args.new_mac:
        parser.error('[-] Please specify a new MAC, use --help for more info')
    return args


def change_mac(interface, new_mac):
    print(f'[+] Changing MAC address for {interface} to {new_mac}')
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])


args = get_arguments()
change_mac(args.interface, args.new_mac)
