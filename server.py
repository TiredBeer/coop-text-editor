import socket
import threading
import os
from client_info import ClientInfo


class Server:
    def __init__(self):
        self.address = ('127.0.0.1', 1488)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.filenames = [f for f in os.listdir('files') if f.endswith('.txt')]



    def run(self):
        self.server_socket.bind(self.address)
        self.server_socket.listen()
        while True:
            conn, addr = self.server_socket.accept()
            client_info = ClientInfo(conn)
            self.clients[addr] = client_info
            threading.Thread(target=self.handle_client, args=[client_info]).start()

    def handle_client(self, client_info):
        while True:
            data = client_info.client_socket.recv(4096).decode()
            print(f'Получено сообщение: {data}')
            if not data:
                break
            data = data.split('\n')
            method = data[0]
            match method:
                case('OPEN'):
                    file_index = int(data[1])
                    client_info.filename = self.filenames[file_index]
                    file_content = self.open_file(client_info.filename)
                    print('kek')
                case('KEY'):
                    print('key')
                    pass
                case('GET_FILES'):
                    filenames = self.get_filenames()
                    client_info.client_socket.sendall(filenames)
                    print('Отправил файлы')

    def get_filenames(self):
        return '\n'.join(self.filenames).encode()

    def open_file(self, filename):
        with open('files/' + filename, 'r') as file:
            return file.readlines()


if __name__ == '__main__':
    server = Server()
    threading.Thread(target=server.run).start()
