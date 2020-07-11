import requests


def download(url):
    response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb') as out_file:
        out_file.write(response.content)


download('https://www.python.org/static/img/python-logo.png')
