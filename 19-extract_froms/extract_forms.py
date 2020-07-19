import requests
from bs4 import BeautifulSoup


def request(url, timeout=3):
    try:
        return requests.get(url, timeout=timeout)
    except requests.exceptions.ConnectionError:
        pass


target_url = 'http://10.0.2.14/mutillidae/index.php?page=dns-lookup.php'
content = request(target_url).content.decode()

parsed_html = BeautifulSoup(content, features='lxml')
forms_list = parsed_html.findAll('form')
print(forms_list)
