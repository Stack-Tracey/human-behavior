import labViewConnector
import game
import time

stream = labViewConnector.LabViewConnector('192.168.56.101', 1337)
game = game.Game(stream)

def get_data(stream):
    x = True
    while x:
        frame = stream.receive_fr()
        msg_type = frame["MsgType"]

        if msg_type == "Frame":
            response = game.play(frame)
            stream.send_fr(response)

        elif msg_type == "Experiment Definition":
            game.experiment_def(frame)

        elif msg_type == "Trial Definition":
            game.trial_def(frame)

        elif msg_type == "Start":
            game.start(frame)

        elif msg_type == "Stop": #TODO handling of pause option
            time.sleep(5)

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
