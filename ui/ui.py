import curses
import threading


class UI:
    def __init__(self, client, text_buffer):
        self.client = client
        self.text_buffer = text_buffer
        self.screen = None
        self.cursor_row = 0
        self.cursor_col = 0

    def run(self):
        curses.wrapper(self.main)

    def main(self, stdscr):
        self.screen = stdscr
        curses.curs_set(1)
        self.screen.clear()
        self.screen.refresh()

        threading.Thread(target=self.render).start()
        while True:
            key = self.screen.getch()
            self.handle_input(key)

    def render(self):
        while True:
            self.screen.clear()
            text = self.text_buffer.get_text()
            self.screen.addstr(text)
            self.screen.move(self.cursor_row, self.cursor_col)
            self.screen.refresh()

    def handle_input(self, key):
        char = chr(key)
        self.client.send_message(f"INSERT\n{self.cursor_row};{self.cursor_col}\n{char}")
        self.cursor_col += 1
