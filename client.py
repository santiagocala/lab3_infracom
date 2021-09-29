import socket
import hashlib
import math
import time
import scapy
from threading import Thread

### Configuration ###
CLIENTS = 10
#####################

SERVER_IP = "localhost"
SERVER_PORT = 8080
BUFFER_SIZE = 1024

log = {}

class SocketThread(Thread):

    def __init__(self, socket, port):
        Thread.__init__(self)
        self.socket = socket
        self.port = port
        self.hash = hash

    def run(self):
        hashBuffer = hashlib.sha256()
        iterations = int(math.ceil(log[self.port]["fileSize"]/BUFFER_SIZE))
        with open("Cliente" + log[self.port]["number"] + "-Prueba-" + str(CLIENTS), "wb") as f:
            initialTime = time.time()
            for i in range(iterations):
                l = self.socket.recv(BUFFER_SIZE)
                f.write(l)
                hashBuffer.update(l)
            self.socket.send(True) # Received last package
            log[self.port]["time"] = int(time.time() - initialTime)
        log[self.port]["success"] = (hash == hashBuffer.hexdigest())
        self.socket.send(log[self.port]["success"])

clients = []

for c in range(CLIENTS):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((SERVER_IP, SERVER_PORT))
    clientPort = clientSocket.getsockname()[1]
    log[clientPort]["number"] = int.from_bytes(clientSocket.recv(1), "big")
    log[clientPort]["fileName"] = clientSocket.recv(7).decode()
    log[clientPort]["fileSize"] = int.from_bytes(clientSocket.recv(4), "big")
    hash = clientSocket.recv(32).hex()
    log[clientPort]["packets"] = 0
    log[clientPort]["bytes"] = 0
    client = SocketThread(clientSocket, clientPort, hash)
    clients.append(client)
    clientSocket.send(True) # Ready to receive

## Start sniff

sniffer = scapy.AsyncSniffer("scr port " + str(SERVER_PORT))
sniffer.start()

for c in clients:
    c.start()

for c in clients:
    c.join()

sniffer.stop()

for packet in sniffer:
    clientPort = packet["TCP"].dport
    log[clientPort]["packets"] = log[clientPort]["packets"] + 1
    log[clientPort]["bytes"] = log[clientPort]["bytes"] + len(packet)

# Create log
# Recorrer clientes
c.socket.close()