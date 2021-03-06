from socket import socket, AF_INET, SOCK_STREAM, MSG_WAITALL
from subprocess import Popen, DEVNULL
from threading import Thread
from datetime import datetime
from math import ceil
from os import remove, mkdir
from os.path import exists
from sys import argv
from hashlib import sha256
from time import time, sleep
from logging import getLogger, CRITICAL
getLogger("scapy").setLevel(CRITICAL) # Hide Scapy warnings
from scapy.all import PcapReader, conf, IP, TCP

CLIENTS = int(argv[1])

INTERFACE = "en0"
SERVER_IP = "192.168.1.155"
SERVER_PORT = 9090
BUFFER_SIZE = 1024

log = {}
if not exists("ArchivosRecibidos"): mkdir("ArchivosRecibidos")

class SocketThread(Thread):

    def __init__(self, socket, port, hash):
        Thread.__init__(self)
        self.socket = socket
        self.port = port
        self.hash = hash

    def run(self):
        hashBuffer = sha256()
        with open("ArchivosRecibidos/Cliente" + str(log[self.port]["number"]) + "-Prueba-" + str(CLIENTS), "wb") as f:
            initialTime = time()
            for i in range(iterations):
                data = self.socket.recv(BUFFER_SIZE, MSG_WAITALL)
                f.write(data)
                hashBuffer.update(data)
            self.socket.sendall(True.to_bytes(1, "big"), MSG_WAITALL) # Received last package
            log[self.port]["time"] = int(time() - initialTime)
            log[self.port]["success"] = (hash == hashBuffer.hexdigest())
            self.socket.sendall(log[self.port]["success"].to_bytes(1, "big"), MSG_WAITALL)

clients = []

for c in range(CLIENTS):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((SERVER_IP, SERVER_PORT))
    clientPort = clientSocket.getsockname()[1]
    log[clientPort] = {}
    log[clientPort]["number"] = int.from_bytes(clientSocket.recv(1, MSG_WAITALL), "big")
    fileName = clientSocket.recv(7, MSG_WAITALL).decode()
    fileSize = int.from_bytes(clientSocket.recv(4, MSG_WAITALL), "big")
    hash = clientSocket.recv(32, MSG_WAITALL).hex()
    log[clientPort]["packets"] = 0
    log[clientPort]["data"] = 0
    client = SocketThread(clientSocket, clientPort, hash)
    clients.append(client)
    clientSocket.sendall(True.to_bytes(1, "big"), MSG_WAITALL) # Ready to receive
    print("Cliente {} listo para recibir".format(log[clientPort]["number"]))

sniffer = Popen(["tcpdump", "-i", INTERFACE, "-s", "66", "-w", "clientsOut.pcap",  "host {} and tcp src port {}".format(SERVER_IP, SERVER_PORT)], stderr = DEVNULL)
sleep(5) # Give time to initialize sniffing

iterations = int(ceil(fileSize / BUFFER_SIZE))
for c in clients:
    c.start()

for c in clients:
    c.join()

sleep(5) # Give time to finish dumping the sniff
sniffer.terminate()

conf.layers.filter([IP, TCP])
for packet in PcapReader("clientsOut.pcap"):
    clientPort = packet[TCP].dport
    log[clientPort]["packets"] = log[clientPort]["packets"] + 1
    log[clientPort]["data"] = log[clientPort]["data"] + packet[IP].len + 14
remove("clientsOut.pcap")

if not exists("Logs"): mkdir("Logs")
with open("Logs/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + "-Clients-log.txt", "w") as f:
    f.write("Archivo: {}, Tama??o(MB): {}\n".format(fileName, fileSize / 10**6))
    for l in log:
        clients[log[l]["number"] - 1].socket.close()
        log[l]["data"] = log[l]["data"] / 10**6
        rate = log[l]["data"]
        if log[l]["time"] != 0: rate = log[l]["data"] / (log[l]["time"])
        f.write("\nCliente: {}, Puerto: {}, Exitoso: {}, PaquetesRecibidos: {}, DatosRecibidos(MB): {}, Tiempo(s): {}, Velocidad(MBps): {}".format(log[l]["number"], l, log[l]["success"], log[l]["packets"], log[l]["data"], log[l]["time"], rate))