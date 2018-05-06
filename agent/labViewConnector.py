import socket
import json


class LabViewConnector:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def receive_fr(self):
        byteA = bytearray()
        while True:
            data = self.sock.recv(1)
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

    def close(self):
        self.sock.close()