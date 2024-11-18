class TextBuffer:
    def __init__(self):
        self.text = ['']
        self.cursor_row = 0
        self.cursor_col = 0

    def insert_init_text(self, row, col, text):
        line = self.text[row]
        self.text[row] = line[:col] + text + line[col:]
        print(f"TextBuffer: Текст после вставки: {self.text}")

    def insert_text(self, row, col, text):
        line = self.text[row]
        self.text[row] = line[:col] + text + line[col:]
        if row == self.cursor_row and col <= self.cursor_col:
            self.cursor_col += len(text)
        print(f"TextBuffer: Текст после вставки: {self.text}")

    def enter(self, row, col):
        line = self.text[row]
        self.text[row] = line[:col]
        self.text.insert(row + 1, line[col:])
        self.cursor_row += 1
        self.cursor_col = len(self.text[row + 1])

    def delete_text(self, row, col, length):
        line = self.text[row]
        self.text[row] = line[:max(0, col - length)] + line[col:]
        print(f"TextBuffer: Текст после удаления: {self.text}")

    def get_text(self):
        return '\n'.join(self.text)


if __name__ == '__main__':
    text_buffer = TextBuffer()
    text_buffer.insert_text(0, 0, 'Hello')
    text_buffer.delete_text(0, 4, 1)
    text_buffer.delete_text(0, 2, 1)
    text_buffer.insert_text(0, 1, 'a')