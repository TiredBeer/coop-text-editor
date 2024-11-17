class TextBuffer:
    def __init__(self):
        self.text = ['']

    def insert_text(self, row, col, text):
        line = self.text[row]
        self.text[row] = line[:col] + text + line[col:]
        print(f"TextBuffer: Текст после вставки: {self.text}")

    def delete_text(self, row, col, length):
        line = self.text[row]
        self.text[row] = line[:max(0, col - length)] + line[col:]
        print(f"TextBuffer: Текст после удаления: {self.text}")


if __name__ == '__main__':
    text_buffer = TextBuffer()
    text_buffer.insert_text(0, 0, 'Hello')
    text_buffer.delete_text(0, 4, 1)
    text_buffer.delete_text(0, 2, 1)
    text_buffer.insert_text(0, 1, 'a')