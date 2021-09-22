import socket
import hashlib
import os
import math
from threading import Thread

SERVER_IP = "localhost"
SERVER_PORT = 8080
BUFFER_SIZE = 1024

CLIENTS = 10
FILE = "file"
FILE_SIZE = int(math.ceil(os.path.getsize(FILE)/BUFFER_SIZE))

class SocketThread(Thread):

    def __init__(self, ip, port, socket, number):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.number = number
        print("Cliente", number, "-", ip, port)

    def run(self):
        self.socket.send(self.number.to_bytes(1, "big"))
        self.socket.send(FILE_SIZE.to_bytes(4, "big"))
        self.socket.send(hash)
        with open(FILE, "rb") as f:
            for b in range(FILE_SIZE):
                self.socket.send(f.read(BUFFER_SIZE))
        self.socket.close()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp.bind((SERVER_IP, SERVER_PORT))
clients = []

with open(FILE, "rb") as f:
    hashBuffer = hashlib.sha256()
    for b in range(FILE_SIZE):
        hashBuffer.update(f.read(BUFFER_SIZE))
hash = hashBuffer.digest()

for c in range(CLIENTS):
    tcp.listen(0)
    (clientSocket, (clientIp, clientPort)) = tcp.accept()
    client = SocketThread(clientIp, clientPort, clientSocket, c + 1)
    clients.append(client)

for c in clients:
    c.start()

for c in clients:
    c.join()