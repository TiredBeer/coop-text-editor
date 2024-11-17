import socket
import threading
from data.text_buffer import TextBuffer


class Server:
    def __init__(self, address):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(address)
        self.text_buffer = TextBuffer()

    def start_server(self):
        self.server_socket.listen()
        while True:
            conn, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=[conn]).start()

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                message = data.decode()
                print(f"Server: Получено сообщение: {message}")

                response = self.handle_message(message)

                client_socket.sendall(response.encode())
        except Exception as e:
            print(f"Server: Ошибка: {e}")
        finally:
            client_socket.close()

    def handle_message(self, message: str) -> str:
        parts = message.split('\n')
        command = parts[0]

        if command == 'INSERT':
            row, col = map(int, parts[1].split(';'))
            text = parts[2]
            self.text_buffer.insert_text(row, col, text)

        return message


if __name__ == '__main__':
    server = Server(('127.0.0.1', 1488))
    server.start_server()
