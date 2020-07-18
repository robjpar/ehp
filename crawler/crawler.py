import requests
from itertools import islice


def request(url, timeout=3):
    try:
        return requests.get(f'http://{url}', timeout=timeout)
    except requests.exceptions.ConnectionError:
        pass


target_url = 'google.com'

with open('subdomains-wordlist.txt', 'r') as wordlist_file:
    n_lines = 10
    for line in islice(wordlist_file, n_lines):
        test_url = f'{line.strip()}.{target_url}'
        response = request(test_url)
        if response:
            print(f'[+] Discovered subdomain --> {test_url}')
