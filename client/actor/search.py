import numpy as np
from heapq import *
from scipy import spatial

class Search:
    def __init__(self, field, targets):
        self.field = field
        self.targets = targets
        self.tar_onhold = 0
        self.nxt_mv = 0

    #manhattan distance
    def heuristic(self, a, b):
        return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

    #A*-search
    def astar(self, array, start, goal):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: self.heuristic(start, goal)}
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
                tentative_g_score = gscore[current] + self.heuristic(current, neighbor)
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
                    fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heappush(oheap, (fscore[neighbor], neighbor))

        return False

    #returns force on ball normalized to [-1, 1]
    def resp_normalized(self, start, goal):
        x_s, y_s = start
        x_g, y_g = goal

        x_r = x_g - x_s
        y_r = y_g - y_s

        m = np.sqrt(pow(x_r, 2) + pow(y_r, 2))

        x_rn = (1 / m) * x_r
        y_rn = (1 / m) * y_r

        return x_rn, y_rn

    def go_for_target(self, ball_pos, radius):
        x_pos, y_pos = ball_pos
        #x,y increased to avoid standing
        x_pos_int = int(x_pos)
        y_pos_int = int(y_pos)
        start = (x_pos_int, y_pos_int)
        r = radius
        print("radius from ball", radius)

        #TODO replacing kdtree with calc of nearest target
        tree = spatial.KDTree(self.targets)
        print("targets from search class", self.targets)

        index = tree.query([start])[1][0]
        goal = self.targets[index]
        print("index and goal from go for target", index, goal)

        nxt_mv = self.nxt_mv

        x, y = goal
        a = (x - r, y - r)
        a_x, a_y = a
        b = (x + r, y + r)
        b_x, b_y = b
        # a <= start <= b
        # or
        c = (x - r, y)
        d = (x + r, y)
        # c <= start <= d
        # or
        e = (x, y - r)
        f = (x, y + r)
        # e <= start <= f
        # or
        g = (x - r, y + r)
        g_x, g_y = g
        h = (x + r, y - r)
        h_x, h_y = h
        # g <= start <= h
        start_x, start_y = start

        print("strat and goal and a, b, c, d", start, goal, a, b, c, d, e, f, g, h)
        if start == goal or nxt_mv == goal or c <= start <= d and e <= start <= f or g_x <= start_x <= h_x and h_y <= start_y <= g_y and a_x <= start_x <= b_x and a_y <= start_y <= b_y:  # tried to fix missing target collision with or statement
            print("first if statement")
            self.targets.pop(index)  # self
            if self.tar_onhold != 0:  # self
                self.targets.append(self.tar_onhold)  # self self

            self.tar_onhold = goal  # self
            print("Target puttetd on hold after start = goal", self.tar_onhold)
            return 0, 0
        else:
            print("x", start, goal)
            path = self.astar(self.field, start, goal)
            print("path from search: ", path)
            step = 1
            if path == False:
                path_len = path
            else:
                path_len = path.__len__()

            if path_len >= step:
                index = path_len - step
                nxt_mv = path[index]
                print("next move starter position 1", nxt_mv)
            elif path_len == False:
                return 0, 0
            else:
                nxt_mv = path.pop()
                print("next move starter position", nxt_mv)

            self.nxt_mv = nxt_mv
            x, y = self.resp_normalized(start, nxt_mv)  # self
            return x, y


