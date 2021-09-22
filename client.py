import socket
import hashlib

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
num_cliente = s.recv(BUFFER_SIZE)
tamanio = int(s.recv(BUFFER_SIZE))
hashsito = hashlib.sha256()
anterior = None
hash_final = None
contador = 0
hash_solicitado = None
with open('received_file' + str(num_cliente) + ".JPG", 'wb') as f:
    print ('file opened')
    while True:
        #print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        if contador == round(tamanio/BUFFER_SIZE):
            hash_final = s.recv(BUFFER_SIZE).decode()
            print("Hashfinal :" + hash_final)
            hash_solicitado = hashsito.hexdigest()
            f.close()
            print('file close()')
            break
        anterior = data
        hashsito.update(data)
        f.write(data)
        contador += 1
    print("Hash final: " + str(hash_final) + " y Hash calculado: " + str(hash_solicitado))
    if hash_final == hash_solicitado:
        print("A momir")

        
print('Successfully get the file')
s.close()
print('connection closed')