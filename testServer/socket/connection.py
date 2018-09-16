import gameServer
from client.actor import game
stream = gameServer.GameServer(1337) #'172.18.101.69'
stream.waitForClient()
game = game.Game(stream)

#gameloop
def send_data(stream):
    x = True
    while x:
        global response
        frame = stream.receive_fr()
        msg_type = frame["MsgType"]
        if msg_type == "Receive Frame":
            print(msg_type)
            nxt_mv = game.play(frame) #{"MsgType": "Receive Frame", "Frame Data": {"X": x, "Y": y}}
            F_x = frame["Frame Data"]['X']
            F_y = frame["Frame Data"]['Y']

            response = {"MsgType":"Frame","Frame Data":{"dt [ms]":257,"Frame Nr.":0,"Trial Elapsed [ms]":0,"Trigger State":544,"Trial Start [ms]":19537131,"Last Frame Start [ms]":19537131,"ODE processed until [ms]":19537131,"Player 1":{"X":512,"Y":384,"F_x":'%c' % F_x,"F_y":'%c' % F_y,"norm_avg_x":-1.0000005960464239951,"norm avg y":0.11531990567377911616,"norm_avg_reshaped_x":-1,"norm avg_reshaped y":0.12813318695257316926},"Player 2":{"X":512,"Y":384,"F_x":0,"F_y":0,"norm_avg_x":1.0000005960464239951,"norm avg y":0.93041839720610064468,"norm_avg_reshaped_x":1,"norm avg_reshaped y":1}}}

        elif some condition:
            response = {"MsgType":"Start","Protocol Version":1}
        elif some other condition:
            response = {"MsgType":"Experiment Definition","Nr_of_Trials":30}
        elif more conditions:
            response = {"MsgType":"Trial Definition","Level Data":{"Trial Type":1,"Trial Duration [ms]":60000,"Nr of Targets":4,"Nr of Obstacles":9,"Ball":{"X":512,"Y":384,"Z":15,"Radius":15},"Targets":{"X":[512,246,778,512],"Y":[691,230,230,384],"Z":[5,5,5,5],"Z_size":[10,10,10,10],"Radius":[35,35,35,35]},"Obstacles":{"X":[512,565,299,328,246,512,604,778,604],"Y":[445,353,261,384,538,77,224,538,544],"Z":[5,5,5,5,5,5,5,5,5],"X_size":[25.600000000000001421,25.600000000000001421,25.600000000000001421,25.600000000000001421,25.600000000000001421,25.600000000000001421,25.600000000000001421,25.600000000000001421,25.600000000000001421],"Y_size":[68.266666666666694141,68.266666666666694141,68.266666666666694141,102.40000000000000568,153.59999999999999432,153.59999999999999432,102.40000000000000568,153.59999999999999432,102.40000000000000568],"Z_size":[10,10,10,10,10,10,10,10,10],"Z_angle_deg":[90,330,210,100,60,180,280,300,280],"geometric type":[1,1,1,1,1,1,1,1,1],"slowdown factor":[0.050000000000000002776,0.050000000000000002776,0.050000000000000002776,0.050000000000000002776,0.050000000000000002776,0.050000000000000002776,0.050000000000000002776,0.050000000000000002776,0.050000000000000002776],"visibility":[3,3,4,4,3,3,3,4,3]},"AI Type":0,"AI 1 Length of Memory":18,"Questionair Text":"I didnt define a cool Questionair Text .. :(","Blink_Wavelength_Screen":40,"Blink_Wavelength_OWG":255,"Screen_Flicker_Target_Radius":20,"Max Force":0.00050000002374872565269,"ShowBar":false,"Nr_of_Frames_to_Skip_at_Start_of_Trial":120,"Show_Fixation_Cross":true,"Visibility per Frame - Ball- Player 1":[],"Visibility per Frame - Targets - Player 1":[],"Visibility per Frame - Obstacles - Player 1":[],"Visibility per Frame - Obstacles 2 - Player 1":[],"Visibility per Frame - Ball- Player 2":[],"Visibility per Frame - Targets - Player 2":[],"Visibility per Frame - Obstacles - Player 2":[],"Visibility per Frame - Obstacles 2 - Player 2":[],"Replay File":"","Replay X Position Ball Player 1":[],"Replay Y Position Ball Player 1":[],"Replay Z Position Ball Player 1":[],"Replay X Position Ball Player 2":[],"Replay Y Position Ball Player 2":[],"Replay Z Position Ball Player 2":[],"Replay Trigger States":[],"Replay X Axis Rotation Ball Player 1":[],"Replay Y Axis Rotation Ball Player 1":[],"Replay Z Axis Rotation Ball Player 1":[],"Replay Angle Rotation Ball Player 1":[],"Replay X Axis Rotation Ball Player 2":[],"Replay Y Axis Rotation Ball Player 2":[],"Replay Z Axis Rotation Ball Player 2":[],"Replay Angle Rotation Ball Player 2":[],"Nr_of_Frames_to_Show_Fixation_Cross":120},"Current Trial Nr.":1}

        else:
            print("overhead has been used---------------------------------------------------------------")
            print(frame)

    stream.send_fr(response)

    send_data(stream)

send_data(stream)
stream.close()
