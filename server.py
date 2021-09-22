import socket
from threading import Thread
from socketserver import ThreadingMixIn
import hashlib
import os

client_capacity = 1
path = ""
contador = 0

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

hashsito = None

class ClientThread(Thread):

    def __init__(self,ip,port,sock,num_cliente):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        self.num_cliente = num_cliente
        print(" New thread started for "+ip+":"+str(port))

    def run(self):
        self.sock.send(str(self.num_cliente).encode())
        filename='IMG_5456 copy.JPG'
        hashsito = hashlib.sha256()
        f = open(filename,'rb')
        self.sock.send(str(os.path.getsize(filename)).encode())
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                hashsito.update(l)
                self.sock.send(l)
                #print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                # resultado = hashsito.hexdigest()
                # print(resultado)
                self.sock.send(hashsito.hexdigest().encode())
                #print(hashsito.hexdigest())
                self.sock.close()
                break

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn,contador)
    contador += 1
    threads.append(newthread)
    print("Se agregó un nuevo thread: Nueva longitud: " + str(len(threads)))
    if len(threads) == client_capacity:
        for thread in threads:
            thread.start()
            thread.join()
        threads.clear()
        print("Nueva longitud: " + str(len(threads)))

for t in threads:
    t.join()