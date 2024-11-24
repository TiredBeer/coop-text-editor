import sys
import os
import json

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
                self.handle_response(response)
            except Exception as e:
                break

    def handle_response(self, response):
        response = json.loads(response)
        self.text_buffer.text = response['TEXT']
        self.text_buffer.cursors = response['POSITIONS']
        cursor = self.text_buffer.cursors[str(self.client_socket.getsockname()[1])]
        self.text_buffer.cursor_row = cursor[0]
        self.text_buffer.cursor_col = cursor[1]


if __name__ == '__main__':
    client = Client()
    client.connect_to_server(('127.0.0.1', 1488))
    ui = UI(client, client.text_buffer)
    ui.run()
