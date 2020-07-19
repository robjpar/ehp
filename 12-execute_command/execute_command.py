# cp execute_command.py /var/www/html/evil-files
# service apache2 start
# http://10.0.2.13/evil-files/

import subprocess

command = '%SystemRoot%\Sysnative\msg.exe * you have been hacked'
subprocess.Popen(command, shell=True)
