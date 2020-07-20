import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

target_url = 'http://10.0.2.14/mutillidae/index.php?page=dns-lookup.php'
response = requests.get(target_url)
content = response.content.decode()

parsed_html = BeautifulSoup(content, features='lxml')
forms_list = parsed_html.findAll('form')

for form in forms_list:
    action = form.get('action')
    post_url = urljoin(target_url, action)
    method = form.get('method')

    inputs_list = form.findAll('input')
    post_data = {}
    for input_ in inputs_list:
        input_name = input_.get('name')
        input_type = input_.get('type')
        input_value = input_.get('value')
        if input_type == 'text':
            input_value = 'test'
        post_data[input_name] = input_value

    response = requests.post(post_url, data=post_data)
    content = response.content.decode()
    print(content)
