import requests
import re
from urllib.parse import urljoin


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

        if url in link and link not in target_links:
            target_links.append(link)
            crawl(link)


target_url = 'http://10.0.2.14'
target_links = []
crawl(target_url)
for link in target_links:
    print(link)
