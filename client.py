import socket
import hashlib
import math

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
num_cliente = s.recv(BUFFER_SIZE)
tamanio = int(s.recv(BUFFER_SIZE))
hashsito = hashlib.sha256()
#restante = tamanio%BUFFER_SIZE
hash_recibido = s.recv(BUFFER_SIZE)
contador = 0
with open('received_file' + str(num_cliente), 'wb') as f:
    print ('file opened')
    while True:
        #print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        if contador == math.ceil((tamanio/BUFFER_SIZE)):
            #ultimafila = s.recv(restante)
            #f.write(ultimafila)
            #hashsito.update(ultimafila)
            #hash_final = s.recv(BUFFER_SIZE)
            #print("Hashfinal :" + str(hash_final))
            hash_calculado = hashsito.hexdigest()
            f.close()
            print('file close()')
            break
        hashsito.update(data)
        f.write(data)
        contador += 1
    print("Hash recibido : " + str(hash_recibido) + " y Hash calculado: " + str(hash_calculado))
    print(contador)
    if hash_recibido == hash_calculado:
        print("A momir")

        
print('Successfully get the file')
s.close()
print('connection closed')