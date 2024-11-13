import socket
import threading
from client_info import ClientInfo


class Server:
    def __init__(self):
        self.address = ('127.0.0.1', 1488)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.file_names = []



    def run(self):
        self.server_socket.bind(self.address)
        self.server_socket.listen()
        while True:
            conn, addr = self.server_socket.accept()
            client_info = ClientInfo(conn)
            self.clients[addr] = client_info
            threading.Thread(target=self.handle_client, args=client_info).start()

    def handle_client(self, client_info):
        while True:
            data = client_info.client_socket.recv(4096).decode()
            if not data:
                break
            data = data.split('\n')
            method = data[0]
            match method:
                case('OPEN'):
                    filename = data[1]
                    client_info.filename = filename
                case('KEY'):
                    pass

    def open_file(self, filename):
        with open(filename, 'r') as file:
            return file.readlines()


if __name__ == '__main__':
    server = Server()
    threading.Thread(target=server.run).start()
