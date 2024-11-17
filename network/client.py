import sys
import os

# Добавляем корневую директорию проекта в путь поиска модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import socket
import threading
from data.text_buffer import TextBuffer
from ui.ui import UI


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.text_buffer = TextBuffer()

    def connect_to_server(self, address):
        self.client_socket.connect(address)
        threading.Thread(target=self.receive_message).start()

    def send_message(self, message):
        self.client_socket.send(message.encode())

    def receive_message(self):
        while True:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                response = data.decode()
                print(f'Client: Получен ответ: {response}')
                self.handle_response(response)
            except Exception as e:
                print(f"Client: Error: {e}")
                break

    def handle_response(self, response):
        parts = response.split('\n')
        command = parts[0]

        if command == 'INSERT':
            row, col = map(int, parts[1].split(';'))
            text = parts[2]
            self.text_buffer.insert_text(row, col, text)


if __name__ == '__main__':
    client = Client()
    client.connect_to_server(('127.0.0.1', 1452))
    ui = UI(client, client.text_buffer)
    ui.run()
    client.send_message('INSERT\n0;0\nHello')
