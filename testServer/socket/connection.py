import gameServer
from client.agent import game
stream = gameServer.GameServer(1337) # '172.18.101.69'
stream.waitForClient()
game = game.Game(stream)

#gameloop
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
