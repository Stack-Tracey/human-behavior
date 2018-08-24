import numpy as np
from heapq import *
from scipy import spatial
#array = np.zeros([20, 20])
#array[4:8, 4:8] = 1
#array[12:16, 10:12] = 1
#array[19:20, 19:20] = 2
#print(array.astype(int))
#start = (1, 1)
#goal = (20, 20)

class Search:
    def __init__(self, field, targets):
        self.field = field
        self.targets = targets
        #print("here comes search field and targets", self.field, self.targets)


    def heuristic(self, a, b):
        return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2


    def astar(self, array, start, goal):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        print("reached astar")
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

    def resp_normalized(self, start, goal):
        print("reached normalization")

        x_s, y_s = start
        print("start values from normalization", x_s, y_s)
        x_g, y_g = goal
        print(x_s, y_s, x_g, y_g)
        x_r = x_g - x_s
        y_r = y_g - y_s

        m = abs(max(x_r, y_r))
        print(m)
        x_rn = x_r / m
        y_rn = y_r / m

        return x_rn, y_rn

    def go_for_target(self, ball_pos):
        print("reached go for target")
        x, y = ball_pos
        x = int(x) + 1
        y = int(y) + 1
        tree = spatial.KDTree(self.targets)
        index = tree.query([(x, y)])[1][0]
        goal = self.targets[index]
        if ball_pos == goal:
            return 0, 0
        else:
            print("here comes astar params", (x, y), goal)
            path = self.astar(self.field, (x, y), goal)
            print("here comes path", path)
            x, y = self.resp_normalized(path.pop(), goal)

            return x, y

