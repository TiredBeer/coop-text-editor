class ClientInfo:
    def __init__(self, socket):
        self.filename = ''
        self.cursor_pos = (0, 0)
        self.client_socket = socket