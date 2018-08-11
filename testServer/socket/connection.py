import virtualPlayerConnector
from client.agent import game
stream = virtualPlayerConnector.VirtualPlayerConnector('192.168.56.101', 1337) # '172.18.101.69'
game = game.Game(stream)

def send_data(stream):
    x = True
    while x:
        frame = stream.receive_fr()
        msg_type = frame["MsgType"]
        if msg_type == "Receive Frame":
            print(msg_type)
            response = game.play(frame)
            stream.send_fr(response)
            #stream.send_fr(\\r)
            #stream.send_fr(\\n)


        else:
            print("overhead has been used---------------------------------------------------------------")
            print(frame)

    send_data(stream)

send_data(stream)
stream.close()
