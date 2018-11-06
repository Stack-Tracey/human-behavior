import socket
import json


class GameServer:
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', port))
        # become a server socket
        self.sock.listen(5)
        self.clientsock = None
        self.trial_def = {"MsgType": "Trial Definition",
                 "Level Data": {"Trial Type": 1, "Trial Duration [ms]": 60000, "Nr of Targets": 4,
                                "Nr of Obstacles": 9, "Ball": {"X": 512, "Y": 384, "Z": 15, "Radius": 15},
                                "Targets": {"X": [512, 246, 778, 512], "Y": [691, 230, 230, 384],
                                            "Z": [5, 5, 5, 5], "Z_size": [10, 10, 10, 10],
                                            "Radius": [35, 35, 35, 35]},
                                "Obstacles": {"X": [512, 459, 725, 420, 328, 420, 512, 604, 778],
                                              "Y": [445, 353, 261, 544, 384, 224, 77, 544, 538],
                                              "Z": [5, 5, 5, 5, 5, 5, 5, 5, 5],
                                              "X_size": [25.0000000000000, 25.0000000000000,
                                                         25.0000000000000, 25.0000000000000,
                                                         25.0000000000000, 25.0000000000000,
                                                         25.0000000000000, 25.0000000000000,
                                                         25.0000000000000],
                                              "Y_size": [68.0000000000000, 68.0000000000000,
                                                         68.0000000000000, 68.0000000000000,
                                                         68.0000000000000, 68.0000000000000,
                                                         68.0000000000000, 68.0000000000000,
                                                         68.0000000000000],
                                              "Z_size": [10, 10, 10, 10, 10, 10, 10, 10, 10],
                                              "Z_angle_deg": [90, 210, 330, 20, 100, 80, 180, 280, 300],
                                              "geometric type": [1, 1, 1, 1, 1, 1, 1, 1, 1],
                                              "slowdown factor": [0.050000000000000002776,
                                                                  0.050000000000000002776,
                                                                  0.050000000000000002776,
                                                                  0.050000000000000002776,
                                                                  0.050000000000000002776,
                                                                  0.050000000000000002776,
                                                                  0.050000000000000002776,
                                                                  0.050000000000000002776,
                                                                  0.050000000000000002776],
                                              "visibility": [3, 3, 3, 3, 3, 4, 3, 4, 4]}, "AI Type": 0,
                                "AI 1 Length of Memory": 18,
                                "Questionair Text": "I didnt define a cool Questionair Text .. :(",
                                "Blink_Wavelength_Screen": 40, "Blink_Wavelength_OWG": 255,
                                "Screen_Flicker_Target_Radius": 20, "Max Force": 0.00050000002374872565269,
                                "ShowBar": "false", "Nr_of_Frames_to_Skip_at_Start_of_Trial": 120,
                                "Show_Fixation_Cross": "true", "Visibility per Frame - Ball- Player 1": [],
                                "Visibility per Frame - Targets - Player 1": [],
                                "Visibility per Frame - Obstacles - Player 1": [],
                                "Visibility per Frame - Obstacles 2 - Player 1": [],
                                "Visibility per Frame - Ball- Player 2": [],
                                "Visibility per Frame - Targets - Player 2": [],
                                "Visibility per Frame - Obstacles - Player 2": [],
                                "Visibility per Frame - Obstacles 2 - Player 2": [], "Replay File": "",
                                "Replay X Position Ball Player 1": [], "Replay Y Position Ball Player 1": [],
                                "Replay Z Position Ball Player 1": [], "Replay X Position Ball Player 2": [],
                                "Replay Y Position Ball Player 2": [], "Replay Z Position Ball Player 2": [],
                                "Replay Trigger States": [], "Replay X Axis Rotation Ball Player 1": [],
                                "Replay Y Axis Rotation Ball Player 1": [],
                                "Replay Z Axis Rotation Ball Player 1": [],
                                "Replay Angle Rotation Ball Player 1": [],
                                "Replay X Axis Rotation Ball Player 2": [],
                                "Replay Y Axis Rotation Ball Player 2": [],
                                "Replay Z Axis Rotation Ball Player 2": [],
                                "Replay Angle Rotation Ball Player 2": [],
                                "Nr_of_Frames_to_Show_Fixation_Cross": 120}, "Current Trial Nr.": 1}

        self.p1_fx = 0
        self.p1_fy = 0
        self.p1_x = 0
        self.p1_y = 0
        self.p2_x = self.p1_x = 512
        self.p2_y = self.p1_y = 384
        self.p2_fx = 0
        self.p2_fy = 0
        self.fr_nr = 0
        self.frame = ""
        self.updateFrame()

    def waitForClient(self):
        print("waiting for client...")
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
        #print(byteA)
        str = byteA.decode("utf-8")
        a = json.loads(str)
        return a

    def send_fr(self, obj):
        str = json.dumps(obj).encode()
        str += b"\r\n"
        self.clientsocket.send(str)

    """

    def send_frame(self, p1_x, p2...):
        self.frame["Player 1"]["X"] = 5
        self.send_fr(self.frame)
        ...
    """

    def close(self):
        self.clientsocket.close()
        self.sock.close()

    def updateFrame(self):
        self.frame = {"MsgType": "Frame",
                      "Frame Data": {"dt [ms]": 0, "Frame Nr.": self.fr_nr, "Trial Elapsed [ms]": 0,
                                     "Trigger State": 544,
                                     "Trial Start [ms]": 0, "Last Frame Start [ms]": 0, "ODE processed until [ms]": 0,
                                     "Player 1": {"X": self.p1_x, "Y": self.p1_y, "F_x": self.p1_fx, "F_y": self.p1_fy,
                                                  "norm_avg_x": 0,
                                                  "norm avg y": 0, "norm_avg_reshaped_x": 0, "norm avg_reshaped y": 0},
                                     "Player 2": {"X": self.p2_x, "Y": self.p2_y, "F_x": self.p2_fx, "F_y": self.p2_fy,
                                                  "norm_avg_x": 0,
                                                  "norm avg y": 0, "norm_avg_reshaped_x": 0, "norm avg_reshaped y": 0}}}

    def getTrialDef(self):
        return self.trial_def

    def getFrame(self):
        return self.frame