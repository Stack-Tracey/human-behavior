import socket
import select
import json

TCP_IP = '172.18.101.206'
TCP_PORT = 1337
BUFFER_SIZE = 1
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((TCP_IP, TCP_PORT))
print()
#s.settimeout(500)
fr_rec = False
byteA = bytearray()
while not fr_rec:
    data = s.recv(BUFFER_SIZE)
    if data[0] == 10:
        fr_rec = True
        print("frame received")
    else:
        byteA.append(data[0])

print(byteA)

a = json.loads(byteA)
print(a)
byteA.append(13)
byteA.append(10)

print(a['X'])
s.send(byteA)
print("a was send")
s.close()