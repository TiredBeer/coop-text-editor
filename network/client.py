import socket
import threading


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
                print(f'Получен ответ: {response}')
                self.handle_response(response)
            except Exception as e:
                print(f"Error: {e}")
                break

    def handle_response(self, response):
        pass


if __name__ == '__main__':
    client = Client()
    client.connect_to_server(('127.0.0.1', 1488))
    client.send_message('Hello')
