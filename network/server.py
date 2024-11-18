import sys
import os

# Добавляем корневую директорию проекта в путь поиска модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import socket
import threading
from data.text_buffer import TextBuffer


class Server:
    def __init__(self, address):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(address)
        self.text_buffer = TextBuffer()
        self.clients = set()

    def start_server(self):
        self.server_socket.listen()
        while True:
            conn, addr = self.server_socket.accept()
            self.clients.add(conn)
            print(f"Server: Новый клиент подключен: {addr}")
            threading.Thread(target=self.handle_client, args=[conn]).start()

    def handle_client(self, client_socket):
        initial_text = "\n".join(self.text_buffer.text)
        client_socket.sendall(f"INSERT_INIT\n0;0\n{initial_text}".encode())

        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                message = data.decode()
                print(f"Server: Получено сообщение: {message}")

                response = self.handle_message(message)

                self.broadcast_update(response)
        except Exception as e:
            print(f"Server: Ошибка: {e}")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()

    def handle_message(self, message: str) -> str:
        parts = message.split('\n')
        command = parts[0]

        if command == 'INSERT':
            row, col = map(int, parts[1].split(';'))
            text = parts[2]
            self.text_buffer.insert_text(row, col, text)

        if command == 'ENTER':
            row, col = map(int, parts[1].split(';'))
            self.text_buffer.enter(row, col)

        return message

    def broadcast_update(self, message):
        for client in self.clients:
            print(self.text_buffer.get_text())
            client.sendall(message.encode())


if __name__ == '__main__':
    server = Server(('127.0.0.1', 1488))
    server.start_server()
