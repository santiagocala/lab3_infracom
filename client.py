import socket

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
with open('received_file', 'wb') as f:
    print ('file opened')
    while True:
        #print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        print('data=%s', (data))
        if not data:
            f.close()
            print('file close()')
            break
        # write data to a file
        f.write(data)
    print(str(hash(f)))


# with open('received_file', 'wb') as f:
#     print 'file opened'
#     anterior = None
#     hash_value = None
#     while True:
#         #print('receiving data...')
#         data = s.recv(BUFFER_SIZE)
#         print('data=%s', (data))
#         if not data:
#             f.close()
#             hash_value = anterior
#             print 'file close()'
#             break
#         # write data to a file
#         anterior = data
#         f.write(data)
    

# with open('received_file', 'wb') as f:
#     print ('file opened')
#     datos = ""
#     hash_value = ""
#     contador = 0
#     while True:
#         #print('receiving data...')
#         data = s.recv(BUFFER_SIZE)
#         if contador == 0:
#             datos = data
#         elif contador == 1:
#             hash_value = data
#         print('data=%s', (data))
#         if not data:
#             f.close()
#             print ('file close()')
#             break
#         contador += 1
#     print("datos: " + str(hash(datos)) + " hash value : " +  str(hash_value))

# with open('received_file', 'wb') as f:
#     while True:
#     print ('file opened')
#         data = s.recv(BUFFER_SIZE)
#         f.write(data)
#         hash_value = s.recv(BUFFER_SIZE)
#         hash_actual = str(hash(f))
#         print(str(hash_value) + " con " + str(hash_actual.encode()))
#         if hash_actual.encode() == hash_value:
#             print("Todo bien")
#         else:
#             print("todo mal")
#         f.close()
#         break
        
print('Successfully get the file')
s.close()
print('connection closed')