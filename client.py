import socket
import hashlib
import math
from threading import Thread

SERVER_IP = "localhost"
SERVER_PORT = 8080
BUFFER_SIZE = 1024

CLIENTS = 10

class SocketThread(Thread):

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))
        number = int.from_bytes(s.recv(1), "big")
        size = int.from_bytes(s.recv(4), "big")
        hash = s.recv(32).hex()
        with open("file" + str(number), "wb") as f:
            hashBuffer = hashlib.sha256()
            for b in range(size):
                l = s.recv(BUFFER_SIZE)
                f.write(l)
                hashBuffer.update(l)
        hashCalculado = hashBuffer.hexdigest()
        s.close()
        print("Cliente", number, "-", "Hash correcto:", hash == hashCalculado)

clients = []

for c in range(CLIENTS):
    client = SocketThread()
    client.start()
    clients.append(client)