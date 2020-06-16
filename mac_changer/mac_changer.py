import subprocess

interface = input('interface > ')
new_mac = input('new MAC > ')
print(f'[+] Changing MAC address for {interface} to {new_mac}')

subprocess.call('ifconfig eth0 down', shell=True)
subprocess.call(f'ifconfig {interface} hw ether {new_mac}', shell=True)
subprocess.call('ifconfig eth0 up', shell=True)
