import numpy
from heapq import *
from scipy import spatial

#bytearray(b'{"MsgType":"Frame",
            # "Frame Data":{"dt [ms]":16,
            #"Frame Nr.":118,
            # "Trial Elapsed [ms]":18446744073709550797,
            # "Trigger State":0,
            # "Trial Start [ms]":7892594,
            #"Last Frame Start [ms]":7891775,
            # "ODE processed until [ms]":7891762,
            #"Player 1":{"X":512,
                        # "Y":384,
                        #"F_x":0,
                        # "F_y":0,
                        # "norm_avg_x":NaN,
                        # "norm avg y":NaN,
                        # "norm_avg_reshaped_x":512,
                        # "norm avg_reshaped y":384},
            # "Player 2":{"X":512,"Y":384,"F_x":0,"F_y":0,"norm_avg_x":NaN,"norm avg y":NaN,"norm_avg_reshaped_x":0,"norm avg_reshaped y":0}}}\r')


#1 - time start of frame
#%       2 - time duration of frame
#%       3 - bimetal deflection 'reshaped' X (norm_avrg_reshaped, i.e. after reshaping to 0.8 ==> 1)####### "norm_avg_reshaped_x":512,
#%       4 - bimetal deflection 'reshaped' Y (norm_avrg_reshaped, i.e. after reshaping to 0.8 ==> 1)#######  "norm avg_reshaped y":384},
#%       5 - X coordinate of ball ###### X
#%       6 - Y coordinate of ball ###### Y
#%       7 - X speed of ball
#%       8 - Y speed of ball
#%       9 - Obstacle hit, yes/no (1/0) - per frame
#%       10 - Target hit, yes/no (1/0) - per frame   % ALWAYS 1 EXCEPT AT END OF THIS TRIAL's FRAMES
#%       11 - Target hit, ID (1,2,3,4) - per frame
#%       12 - Obstacle hit, yes/no (1/0) - collection events ONLY
#%       13 - Target hit, yes/no (1/0) - collection events ONLY
#%       14 - Target hit, ID (1,2,3,4) - collection events ONLY
#%       15 - bimetal deflection 'raw' X (mean of AI_x_Samples)
#%       16 - bimetal deflection 'raw' Y (mean of AI_y_Samples)
#%       17 - bimetal deflection 'medium' X (norm_avrg, i.e. after calibration) ####### "norm_avg_reshaped_x":512,
#%       18 - bimetal deflection 'medium' Y (norm_avrg, i.e. after calibration) ####### "norm avg y":NaN,
#%       19 - X force on ball (Fx, considering influence of one or both players, dep. on trial type)
#%       20 - Y force on ball (Fy, considering influence of one or both players, dep. on trial type)
#%       21 - marker of especially good play
#%       22 - 30: infos on unilateral obstacle visibility
#%       31 - close-to-how-many-regions
#%       32 - who_is_seeing (nobody = 0, P1 = 1, P2 = 2, both = 3)

array = numpy.zeros([20, 20])
array[4:8, 4:8] = 2
array[12:16, 10:12] = 1
array[17:20, 13:20] = 2

start = (1, 1)
goal = (19, 19)
print(array.astype(int), start, goal)
def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2


def astar(array, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))

    while oheap:
        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))

    return False




#airports = [(10, 10), (20, 20), (30, 30), (40, 40)]
#tree = spatial.KDTree(airports)
#print(tree.query([(29, 29)]))
#a = tree.query([(29, 29)])[1][0]
#print(a)

#tup = [(3,4), (43, 6), (5,9), (20, 100)]

#print(sorted(tup))
a = astar(array, start, goal)
print(a)

nmap = numpy.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

b = astar(array, start, goal)
print(b)
print(b.pop())
print(b.pop())
print(b)

#if not self.path:
   # self.path = self.search.go_for_target((p1_x, p1_y))
#if not self.path:
    #x, y = p1_x, p1_y
   # print("here somes p1 x p1 y", p1_x, p1_y)
#else:
   # x, y = self.path.pop()

start = (2, 1)
goal = (5, 3)

def resp_normalized(start, goal):
    x_s, y_s = start
    x_g, y_g = goal
    print(x_s, y_s, x_g, y_g)
    x_r = x_g - x_s
    y_r = y_g - y_s

    #old calculation
    #m = abs(max(x_r, y_r))
    #print(m)
    #x_rn = x_r / m
    #y_rn = y_r / m

    m = numpy.sqrt(pow(x_r, 2) + pow(y_r, 2))
    print(m)
    x_rn = x_r / m
    y_rn = y_r / m
    return x_rn, y_rn

    return x_rn, y_rn

a = resp_normalized((43, 498), (587, 13))
b = resp_normalized((700, 1), (1, 700))
c = resp_normalized((430, 689), (1200, 130))
print(a, b, c)