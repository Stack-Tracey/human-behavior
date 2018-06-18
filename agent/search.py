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
        print("reached heuristik")
        return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2


    def astar(self, array, start, goal):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: self.heuristic(start, goal)}
        oheap = []
        print("here comes fscore from astar", fscore)
        heappush(oheap, (fscore[start], start))
        print("here comes oheap", oheap)

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

    def go_for_target(self, ball_pos):
        x, y = ball_pos
        print("here comes x, y", x, y)
        tree = spatial.KDTree(self.targets)
        index = tree.query([(x, y)])[1][0]

        goal = self.targets[index]
        resp = self.astar(self.field, ball_pos, goal)
        print("here comes resp", resp)
        return resp
        #astar(array, start, goal)

