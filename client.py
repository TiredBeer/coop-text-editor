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

    def print_files(self, stdscr, files):
        for i in range(len(files)):
            stdscr.addstr(i, 0, '   ' + files[i])

    def select_file(self, stdscr):
        request = 'GET_FILES\n'
        self.send_data(request)
        files = self.client_socket.recv(4096).decode().split('\n')
        self.print_files(stdscr, files)
        self.print_pointer(stdscr, len(files))


    def print_pointer(self, stdscr, length):
        curses.curs_set(0)
        pointer_pos_y = 0
        stdscr.addstr(pointer_pos_y, 0, '->')
        while True:
            key = stdscr.getch()
            match key:
                case(10):
                    stdscr.clear()
                    message = f'OPEN\n{pointer_pos_y}'
                    self.send_data(message)
                    file_content = self.client_socket.recv(4096).decode()
                    stdscr.addstr(0, 0, file_content)
                    break
                case(curses.KEY_UP):
                    if pointer_pos_y > 0:
                        stdscr.addstr(pointer_pos_y, 0, '  ')
                        pointer_pos_y -= 1
                case(curses.KEY_DOWN):
                    if pointer_pos_y < length - 1:
                        stdscr.addstr(pointer_pos_y, 0, '  ')
                        pointer_pos_y += 1
            stdscr.addstr(pointer_pos_y, 0, '->')


def main(stdscr, host, port):
    client = Client(host, port)
    client.connect_to_server()
    client.select_file(stdscr)
    while True:
        key = str(stdscr.getch())
        client.send_data(key)
        stdscr.addstr(key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True,
                        help='IP-адрес сервера')
    parser.add_argument('--port', type=int, required=True,
                        help='Порт подкючения')
    args = parser.parse_args()
    curses.wrapper(main, args.host, args.port)
