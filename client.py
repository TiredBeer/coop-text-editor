import argparse
import curses
import socket



class Client:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)

    def connect_to_server(self):
        self.client_socket.connect(self.server_address)

    def send_data(self, data: str):
        self.client_socket.send(data.encode())


def main(stdscr, host, port):
    client = Client(host, port)
    client.connect_to_server()
    while True:
        key = str(stdscr.getch())
        client.send_data(key)
        stdscr.addstr(key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True,
                        help='IP-адрес хоста, на котором будет запущен сервер.')
    parser.add_argument('--port', type=int, required=True,
                        help='Порт подкючения')
    args = parser.parse_args()
    curses.wrapper(main, args.host, args.port)
