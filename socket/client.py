import socket
import select
import json

class LabViewConnector:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def receive_fr(self):
        byteA = bytearray()
        while True:
            data = self.sock.recv(BUFFER_SIZE)
            if data[0] == 10:
                break
            else:
                byteA.append(data[0])
        print(byteA)
        str = byteA.decode("utf-8")
        a = json.loads(str)
        return a

    def send_fr(self, obj):
        str = json.dumps(obj).encode()
        self.sock.send(str)



TCP_IP = '192.168.56.101'
TCP_PORT = 1337
BUFFER_SIZE = 1
MESSAGE = "Hello, World!"


while True:
    a = receive_fr()
    b = {'x' : 5} #placeholder for calculating stuff
    con.send_fr(b)

con.close()

print()
#s.settimeout(500)
fr_rec = False




#a = receive_fr(s)

b = {}
b['x'] = 5
b['y'] = 10

send_fr(s, b)
print(str)


print(a['X'])
#s.send(byteA)
print("a was send")
s.close()