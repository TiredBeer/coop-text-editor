class TextBuffer:
    def __init__(self):
        self.text = ['']
        self.cursor_row = 0
        self.cursor_col = 0
        self.cursors = {}

    def insert_init_text(self, row, col, text):
        line = self.text[row]
        self.text[row] = line[:col] + text + line[col:]
        print(f"TextBuffer: Текст после вставки: {self.text}")

    def insert_text(self, row, col, text, client):
        line = self.text[row]
        self.text[row] = line[:col] + text + line[col:]
        if row == self.cursors[client][0] and col <= self.cursors[client][1]:
            self.cursors[client][1] += len(text)
        print(f"TextBuffer: Текст после вставки: {self.text}")

    def enter(self, row, col, client):
        line = self.text[row]
        self.text[row] = line[:col]
        self.text.insert(row + 1, line[col:])
        self.cursors[client][0] += 1
        self.cursors[client][1] = 0

    def delete_text(self, row, col, length, client):
        client_row = self.cursors[client][0]
        client_col = self.cursors[client][1]
        line = self.text[row]
        self.text[row] = line[:max(0, col - length)] + line[col:]
        if col == 0:
            client_row = max(0, client_row - 1)
            client_col = len(self.text[client_row])
            self.insert_init_text(client_row, client_col, self.text[row])
            self.text.remove(self.text[row])
        else:
            client_col -= 1
        self.cursors[client] = [client_row, client_col]
        print(f"TextBuffer: Текст после удаления: {self.text}")

    def get_text(self):
        return '\n'.join(self.text)


if __name__ == '__main__':
    text_buffer = TextBuffer()
    text_buffer.insert_text(0, 0, 'Hello')
    text_buffer.delete_text(0, 4, 1)
    text_buffer.delete_text(0, 2, 1)
    text_buffer.insert_text(0, 1, 'a')