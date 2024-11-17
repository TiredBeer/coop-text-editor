import socket
import threading


class Server:
    def __init__(self, address):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(address)

    def start_server(self):
        self.server_socket.listen()
        while True:
            conn, addr = self.server_socket.accept()
            client_handler = ClientHandler(conn)
            threading.Thread(target=client_handler.run).start()



class ClientHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def run(self):
        try:
            while True:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                message = data.decode()
                print(f"Получено сообщение: {message}")

                response = self.handle_message(message)

                self.client_socket.sendall(response.encode())
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            self.client_socket.close()

    def handle_message(self, message: str) -> str:
        return message


if __name__ == '__main__':
    server = Server(('127.0.0.1', 1488))
    server.start_server()
