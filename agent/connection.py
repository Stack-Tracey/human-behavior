import labViewConnector
import game
trial_def = []
play = []
experiment_def = []
overhead = []
stream = labViewConnector.LabViewConnector('192.168.56.101', 1337)
game = game.Game(stream)

def get_data(stream):
    x = True
    while x:
        frame = stream.receive_fr()
        msg_type = frame["MsgType"]
        if msg_type == "Frame":
            play.append(frame)
            game.play(frame)
            print("package received")
            print(play)
        elif msg_type == "Experiment Definition":
            experiment_def.append(frame)
            game.experiment_def(frame)
        elif msg_type == "Trial Definition":
            trial_def.append(frame)
            game.trial_def(frame)
            print("package received")
            print(trial_def)
        elif msg_type == "Start":
            game.start(frame)
            print(frame)
        elif msg_type == "End":
            x = False
            return x
            get_data(stream)
        else:
            overhead.append(a)
            #b = game.response() # placeholder for calculating stuff
            #con.send_fr(b)
    get_data(stream)


get_data(stream)
print("package received:")
print(overhead)
print(experiment_def)
print(trial_def)
print(play)
stream.close()
