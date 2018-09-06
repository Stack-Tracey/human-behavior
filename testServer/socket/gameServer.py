import socket
import json


class GameServer:
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', port))
        # become a server socket
        self.sock.listen(5)
        self.clientsock = None

    def waitForClient(self):
        if self.clientsock:
            self.clientsocket.close()
        (self.clientsocket, address) = self.sock.accept()

    def receive_fr(self):
        byteA = bytearray()
        while True:
            data = self.clientsocket.recv(1)
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
        str += b"\r\n"
        self.clientsocket.send(str)

    def close(self):
        self.clientsocket.close()
        self.sock.close()