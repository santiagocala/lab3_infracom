import socket
from threading import Thread
from socketserver import ThreadingMixIn

client_capacity = 4
path = ""
active_connections = 0

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

hashsito = None

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print(" New thread started for "+ip+":"+str(port))

    def run(self):
        filename='archivo100.txt'
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                #print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                hashsito = str(hash(f))
                f.close()
                self.sock.close()
                break
        print(hashsito)

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
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