import requests
import re
import urllib.parse


def extract_links_from(url):
    response = requests.get(url)
    content = response.content.decode()
    return re.findall('href="(.*?)"', content)


target_url = 'http://10.0.2.14/mutillidae'
href_links = extract_links_from(target_url)

for link in href_links:
    link = urllib.parse.urljoin(target_url, link)

    if target_url in link:
        print(link)
