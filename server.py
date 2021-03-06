from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, MSG_WAITALL
from subprocess import Popen, DEVNULL
from threading import Thread
from datetime import datetime
from math import ceil
from os import remove, mkdir
from os.path import getsize, exists
from sys import argv
from hashlib import sha256
from time import time, sleep
from logging import getLogger, CRITICAL
getLogger("scapy").setLevel(CRITICAL) # Hide Scapy warnings
from scapy.all import PcapReader, conf, IP, TCP

CLIENTS = int(argv[1])
FILE_NAME = str(argv[2])

INTERFACE = "enp0s3"
SERVER_IP = "192.168.1.155"
SERVER_PORT = 9090
BUFFER_SIZE = 1024
FILE_SIZE = getsize(FILE_NAME)
ITERATIONS = int(ceil(FILE_SIZE / BUFFER_SIZE))

log = {}

class SocketThread(Thread):

    def __init__(self, socket, port):
        Thread.__init__(self)
        self.socket = socket
        self.port = port

    def run(self):
        with open(FILE_NAME, "rb") as f:
            initialTime = time()
            for i in range(ITERATIONS):
                self.socket.sendall(f.read(BUFFER_SIZE), MSG_WAITALL)
            self.socket.recv(1, MSG_WAITALL) # Received last package
            log[self.port]["time"] = int(time() - initialTime)
            log[self.port]["success"] = bool.from_bytes(self.socket.recv(1, MSG_WAITALL), "big") 

with open(FILE_NAME, "rb") as f:
    hashBuffer = sha256()
    for i in range(ITERATIONS):
        hashBuffer.update(f.read(BUFFER_SIZE))
    hash = hashBuffer.digest()

tcpSocket = socket(AF_INET, SOCK_STREAM)
tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSocket.bind((SERVER_IP, SERVER_PORT))
clients = []

for c in range(CLIENTS):
    tcpSocket.listen(CLIENTS)
    (clientSocket, (clientIp, clientPort)) = tcpSocket.accept()
    log[clientPort] = {}
    log[clientPort]["number"] = c + 1
    log[clientPort]["packets"] = 0
    log[clientPort]["data"] = 0
    clientSocket.sendall(log[clientPort]["number"].to_bytes(1, "big"), MSG_WAITALL)
    clientSocket.sendall(FILE_NAME.encode(), MSG_WAITALL)
    clientSocket.sendall(FILE_SIZE.to_bytes(4, "big"), MSG_WAITALL)
    clientSocket.sendall(hash, MSG_WAITALL)
    client = SocketThread(clientSocket, clientPort)
    clients.append(client)
    clientSocket.recv(1, MSG_WAITALL) # Ready to receive

sniffer = Popen(["tcpdump", "-i", INTERFACE, "-s", "66", "-w", "serverOut.pcap",  "host {} and tcp src port {}".format(SERVER_IP, SERVER_PORT)], stderr = DEVNULL)
sleep(5) # Give time to initialize sniffing

for c in clients:
    c.start()

for c in clients:
    c.join()

sleep(5) # Give time to finish dumping the sniff
sniffer.terminate()

conf.layers.filter([IP, TCP])
for packet in PcapReader("serverOut.pcap"):
    clientPort = packet[TCP].dport
    log[clientPort]["packets"] = log[clientPort]["packets"] + 1
    log[clientPort]["data"] = log[clientPort]["data"] + packet[IP].len + 14
remove("serverOut.pcap")

if not exists("Logs"): mkdir("Logs")
with open("Logs/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + "-Server-log.txt", "w") as f:
    f.write("Archivo: {}, Tama??o(MB): {}\n".format(FILE_NAME, FILE_SIZE / 10**6))
    for l in log:
        clients[log[l]["number"] - 1].socket.close()
        log[l]["data"] = log[l]["data"] / 10**6
        rate = log[l]["data"]
        if log[l]["time"] != 0: rate = log[l]["data"] / (log[l]["time"])
        f.write("\nCliente: {}, Puerto: {}, Exitoso: {}, PaquetesEnviados: {}, DatosEnviados(MB): {}, Tiempo(s): {}, Velocidad(MBps): {}".format(log[l]["number"], l, log[l]["success"], log[l]["packets"], log[l]["data"], log[l]["time"], rate))