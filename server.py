import socket
import hashlib
import os
import math
import time
import scapy
from threading import Thread

### Configuration ###
CLIENTS = 10
FILE_NAME = "100.txt"
#####################

SERVER_IP = "localhost"
SERVER_PORT = 8080
BUFFER_SIZE = 1024
FILE_SIZE = os.path.getsize(FILE_NAME)
ITERATIONS = int(math.ceil(FILE_SIZE/BUFFER_SIZE))

log = {}

class SocketThread(Thread):

    def __init__(self, socket, port):
        Thread.__init__(self)
        self.socket = socket
        self.port = port

    def run(self):
        with open(FILE_NAME, "rb") as f:
            initialTime = time.time()
            for i in range(ITERATIONS):
                self.socket.send(f.read(BUFFER_SIZE))
            self.socket.recv(1) # Received last package
            log[self.port]["time"] = int(time.time() - initialTime)
        log[self.port]["success"] = bool.from_bytes(self.socket.recv(1), "big") 

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp.bind((SERVER_IP, SERVER_PORT))
clients = []

with open(FILE_NAME, "rb") as f:
    hashBuffer = hashlib.sha256()
    for i in range(ITERATIONS):
        hashBuffer.update(f.read(BUFFER_SIZE))
hash = hashBuffer.digest()

for c in range(CLIENTS):
    tcp.listen(0)
    (clientSocket, (clientIp, clientPort)) = tcp.accept()
    log[clientPort] = {}
    log[clientPort]["number"] = c + 1
    log[clientPort]["packets"] = 0
    log[clientPort]["bytes"] = 0
    clientSocket.send(log[clientPort]["number"].to_bytes(1, "big"))
    clientSocket.send(FILE_NAME.encode())
    clientSocket.send(FILE_SIZE.to_bytes(4, "big"))
    clientSocket.send(hash)
    client = SocketThread(clientSocket, clientPort)
    clients.append(client)
    clientSocket.recv(1) # Ready to receive

sniffer = scapy.AsyncSniffer("scr port " + str(SERVER_PORT))
sniffer.start()

for c in clients:
    c.start()

sniffer.stop

for c in clients:
    c.join()

for packet in sniffer:
    clientPort = packet["TCP"].dport
    log[clientPort]["packets"] = log[clientPort]["packets"] + 1
    log[clientPort]["bytes"] = log[clientPort]["bytes"] + len(packet)

# Create log
#Recorrer clientes
c.socket.close()