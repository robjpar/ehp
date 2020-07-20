import requests
import re
from urllib.parse import urljoin


target_url = 'http://10.0.2.14/mutillidae/'
target_links = []


def extract_links_from(url):
    response = requests.get(url)
    content = response.content.decode(errors='ignore')
    return re.findall('href="(.*?)"', content)


def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urljoin(url, link)

        if '#' in link:
            link = link.split('#')[0]

        if target_url in link and link not in target_links:
            print(f'Found link > {link}')
            target_links.append(link)
            crawl(link)


crawl(target_url)
