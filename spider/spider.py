import requests
import re


def request(url, timeout=3):
    try:
        return requests.get(f'http://{url}', timeout=timeout)
    except requests.exceptions.ConnectionError:
        pass


target_url = '10.0.2.14/mutillidae'

response = request(target_url)
content = response.content.decode()
href_links = re.findall('href="(.*?)"', content)
print(href_links)
