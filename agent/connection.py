import labViewConnector
import game

trial_defs = []
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

        if msg_type == "Frame" and frame['Frame Data']['Frame Nr.'] != 0:
            game.play(frame)
            play.append(frame)
            #print("package received")
            #print(play)
        elif msg_type == "Experiment Definition":
            experiment_def.append(frame)
            game.experiment_def(frame)
            #print("package received")
            #print(experiment_def)
        elif msg_type == "Trial Definition":
            trial_defs.append(frame)
            #print("package received")
            #print(trial_defs)
        elif msg_type == "Start":
            game.start(frame)
            #print("package received")
            #print(frame)
        elif msg_type == "End":
            x = False
            return x
            #get_data(stream)
        elif msg_type == "Frame" and frame['Frame Data']['Frame Nr.'] == 0:
            print("sorting works")
            print(trial_defs)
            game.trial_def(trial_defs)
            game.play(frame)
            play.append(frame)
        else:
            overhead.append(frame)
            #b = game.response() # placeholder for calculating stuff
            #con.send_fr(b)

    get_data(stream)


get_data(stream)
#print("package received:")
#print(overhead)
#print(experiment_def)
#print(trial_defs)
#print(play)
stream.close()
