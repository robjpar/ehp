import requests
from itertools import islice


def request(url, timeout=3):
    try:
        return requests.get(f'http://{url}', timeout=timeout)
    except requests.exceptions.ConnectionError:
        pass


target_url = 'google.com'
n_lines = 3

with open('subdomains-wordlist.txt', 'r') as wordlist_file:
    for line in islice(wordlist_file, n_lines):
        test_url = f'{line.strip()}.{target_url}'
        response = request(test_url)
        if response:
            print(f'[+] Discovered subdomain --> {test_url}')


target_url = '10.0.2.14/mutillidae'
n_lines = 5000

with open('files-and-dirs-wordlist.txt', 'r') as wordlist_file:
    for line in islice(wordlist_file, n_lines):
        test_url = f'{target_url}/{line.strip()}'
        response = request(test_url)
        if response:
            print(f'[+] Discovered url --> {test_url}')
