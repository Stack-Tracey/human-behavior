import labViewConnector
from client.agent import game
stream = labViewConnector.LabViewConnector('172.18.101.69', 1337) # '192.168.56.101'
game = game.Game(stream)

def get_data(stream):
    x = True
    while x:
        frame = stream.receive_fr()
        msg_type = frame["MsgType"]

        if msg_type == "Frame":
            print(msg_type)
            response = game.play(frame)
            stream.send_fr(response)
            #stream.send_fr(\\r)
            #stream.send_fr(\\n)

        elif msg_type == "Experiment Definition":
            game.experiment_def(frame)

        elif msg_type == "Trial Definition":
            game.trial_def(frame)

        elif msg_type == "Start":
            game.start(frame)

        elif msg_type == "Stop": #TODO handling of pause option
            print("opponent paused") #time.sleep(5)

        elif msg_type == "End":
            x = False
            return x
            #get_data(stream)
        else:
            print("overhead has been used---------------------------------------------------------------")
            print(frame)

    get_data(stream)

get_data(stream)
stream.close()
