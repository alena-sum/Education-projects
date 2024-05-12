import socket
from config import *

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 2345
        self.address = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.address)
        return self.client.recv(POCKET_SIZE).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(POCKET_SIZE).decode()
            return reply
        except socket.error as error:
            return str(error)
