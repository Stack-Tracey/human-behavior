import numpy as np
from heapq import *
from scipy import spatial

class Search:
    def __init__(self, field, targets):
        self.field = field
        self.targets = targets
        self.tar_onhold = 0
        self.reint = 1

    #manhattan distance
    def heuristic(self, a, b):
        return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

    #A*-search
    def astar(self, array, start, goal):
        print("reached astar")
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
        print("reached normalization")

        x_s, y_s = start
        x_g, y_g = goal
        print("start/goal values for normalization x_s y_s, x_g y_g", x_s, y_s, x_g, y_g)

        x_r = x_g - x_s
        y_r = y_g - y_s

        #TODO wrong calculation, the ball moves into the wrong direction
        #  m = abs(max(x_r, y_r)) did not workout, new try:
        m = np.sqrt(pow(x_r, 2) + pow(y_r, 2))
        print("m from normalization", m)

        x_rn = (1 / m) * x_r
        y_rn = (1 / m) * y_r

        return x_rn, y_rn

    def go_for_target(self, ball_pos):
        print("reached go for target")

        x, y = ball_pos
        #x,y increased to avoid standing
        x = int(x) + 1
        y = int(y) + 1

        #TODO replacing kdtree with calc of nearest target
        tree = spatial.KDTree(self.targets)
        print("targets from search class", self.targets)

        index = tree.query([(x, y)])[1][0]
        goal = self.targets[index]
        print("index and goal from go for target", index, goal)

        if self.reint == 0:
            print("tar_onhold", self.tar_onhold)
            self.targets.append(self.tar_onhold)
            sorted(self.targets)
            #neccesary for kdtree to determine the nearest target,
            #kdtree does not work proper so will be be replaced
            print("targets from search after sorting", self.targets)
        if ball_pos == goal:
            self.tar_onhold = goal
            self.targets.pop(index)
            self.reint = 200
            return 0, 0
        else:
            print("astar params: ", (x, y), goal)
        path = self.astar(self.field, (x, y), goal)
        print("path to target returned by search in search.py: ", path)
        #if collected coin, don't move
        if path == []:
            x = 0
            y = 0
            return x, y
        #else get the next step on path to move to
        else:
            x, y = self.resp_normalized(path.pop(), goal)
            print("here comes reint", self.reint)
            return x, y

