import curses
import socket


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('127.0.0.1', 1488)

    def connect_to_server(self):
        self.client_socket.connect(self.server_address)

    def send_data(self, data: str):
        self.client_socket.send(data.encode())


def main(stdscr):
    client = Client()
    client.connect_to_server()
    while True:
        key = str(stdscr.getch())
        client.send_data(key)
        stdscr.addstr(key)


if __name__ == '__main__':
    curses.wrapper(main)
