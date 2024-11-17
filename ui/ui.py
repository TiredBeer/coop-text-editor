import curses


class UI:
    def __init__(self, client, text_buffer):
        self.client = client
        self.text_buffer = text_buffer
        self.screen = None

    def run(self):
        curses.wrapper(self.main)

    def main(self, stdscr):
        self.screen = stdscr
        curses.curs_set(1)
        self.screen.nodelay(True)
        self.screen.clear()
        self.screen.refresh()

        while True:
            self.render()
            key = self.screen.getch()
            self.handle_input(key)

    def render(self):
        self.screen.clear()
        text = self.text_buffer.get_text()
        self.screen.addstr(text)
        self.screen.move(self.text_buffer.cursor_row, self.text_buffer.cursor_col)
        self.screen.refresh()

    def handle_input(self, key):
        if key == -1:
            return
        char = chr(key)
        self.client.send_message(f"INSERT\n{self.text_buffer.cursor_row};{self.text_buffer.cursor_col}\n{char}")
