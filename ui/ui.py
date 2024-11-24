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
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.curs_set(0)
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
        self.render_cursors(self.screen)
        self.screen.move(self.text_buffer.cursor_row, self.text_buffer.cursor_col)
        self.screen.refresh()

    def handle_input(self, key):
        if key == -1:
            return
        elif key in [curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT]:
            self.move_cursor(key)
            self.client.send_message(f"UPDATE_POS\n{self.text_buffer.cursor_row};{self.text_buffer.cursor_col}")
        elif key == 10:
            self.client.send_message(f"ENTER\n{self.text_buffer.cursor_row};{self.text_buffer.cursor_col}")
        elif key == 8:
            self.client.send_message(f"DELETE\n{self.text_buffer.cursor_row};{self.text_buffer.cursor_col}\n1")
        else:
            char = chr(key)
            self.client.send_message(f"KEY\n{key}")
            self.client.send_message(f"INSERT\n{self.text_buffer.cursor_row};{self.text_buffer.cursor_col}\n{char}")

    def move_cursor(self, key):
        x = self.text_buffer.cursor_col
        y = self.text_buffer.cursor_row
        max_x = len(self.text_buffer.text[y])
        max_y = len(self.text_buffer.text) - 1
        if key == curses.KEY_RIGHT:
            self.text_buffer.cursor_col = min(max_x, x + 1)
        elif key == curses.KEY_LEFT:
            self.text_buffer.cursor_col = max(0, x - 1)
        elif key == curses.KEY_UP:
            self.text_buffer.cursor_row = max(0, y - 1)
        elif key == curses.KEY_DOWN:
            self.text_buffer.cursor_row = min(max_y, y + 1)

        if self.text_buffer.cursor_col > len(self.text_buffer.text[self.text_buffer.cursor_row]) - 1:
            self.text_buffer.cursor_col = len(self.text_buffer.text[self.text_buffer.cursor_row])

    def render_cursors(self, screen):
        print(self.text_buffer.cursors)
        for cursor in self.text_buffer.cursors:
            color = 1
            if cursor == str(self.client.client_socket.getsockname()[1]):
                color = 2
            cursor_row, cursor_col = self.text_buffer.cursors[cursor]
            print(cursor_row, cursor_col)
            try:
                char = self.text_buffer.text[cursor_row][cursor_col]
                screen.addch(cursor_row, cursor_col, char, curses.color_pair(color))
            except IndexError:
                screen.addch(cursor_row, cursor_col, ' ', curses.color_pair(color))
