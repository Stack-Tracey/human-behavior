import labViewConnector
import sys
#from client.actor import game
sys.path.append('../')
from actor import game

lab = '172.18.101.69'
vbx = '192.168.56.101'
localhorst = '127.0.0.1'

stream = labViewConnector.LabViewConnector(localhorst, 1337)
game = game.Game(stream)

#handles incomming frames according to their types
def get_data(stream):
    x = True
    #clock = pygame.time.Clock()
    while x:
        #.tick(30)
        frame = stream.receive_fr()
        msg_type = frame["MsgType"]

        if msg_type == "Frame":
            response = game.play(frame)
            stream.send_fr(response)

        elif msg_type == "Experiment Definition":
            game.experiment_def(frame)

        elif msg_type == "Trial Definition":
            game.trial_def(frame)
            print("frame received")

        elif msg_type == "Start":
            game.start(frame)

        elif msg_type == "Stop": #TODO handling of pause option
            print("opponent paused") #time.sleep(5)

        elif msg_type == "End":
            x = False
            return x

        else:
            print("overhead has been used---------------------------------------------------------------")
            print(frame)


if "profile" in sys.argv:
    import hotshot
    import hotshot.stats
    import tempfile
    import os

    print("Test")
    profile_data_fname = tempfile.mktemp("prf")
    prof = hotshot.Profile(profile_data_fname)
    prof.run('get_data(stream)')
    del prof
    s = hotshot.stats.load(profile_data_fname)
    s.strip_dirs()
    print("cumulative\n\n")
    s.sort_stats('cumulative').print_stats()
    print("By time.\n\n")
    s.sort_stats('time').print_stats()
    del s
    # clean up the temporary file name.
    try:
        os.remove(profile_data_fname)
    except:
        # may have trouble deleting ;)
        pass
else:
    get_data(stream)
stream.close()