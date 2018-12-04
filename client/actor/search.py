import numpy as np
from heapq import *
from scipy import spatial

class Search:
    def __init__(self, field, targets):
        self.field = field
        self.targets = targets
        self.tar_onhold = 0
        self.nxt_mv = 0
        self.counter = 19
        self.path = False

    #L1-norm manhattan distance as heuristik for astar
    def heuristic(self, a, b):
        return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

    #A*-search
    def astar(self, array, start, goal):
        open_heap = []
        came_from = {}
        close_set = set()
        gscore = {start: 0}
        hscore = {start: self.heuristic(start, goal)}
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        heappush(open_heap, (hscore[start], start))

        while open_heap:
            current = heappop(open_heap)[1]
            if current == goal:
                data = []

                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data

            close_set.add(current)
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                tent_g_score = gscore[current] + self.heuristic(current, neighbor)
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

                if neighbor in close_set and tent_g_score >= gscore.get(neighbor, 1024):
                    continue

                if tent_g_score < gscore.get(neighbor, 1024) or neighbor not in [i[1] for i in open_heap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tent_g_score
                    hscore[neighbor] = tent_g_score + self.heuristic(neighbor, goal)
                    heappush(open_heap, (hscore[neighbor], neighbor))

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



        """
         samples points along a line from point A= checkpoint to point B = current_point_next at a certain granularity
         (typically we use one-fifth of a tile width), checking at each point whether the unit overlaps
         any neighboring blocked tile. (Using the width of the unit, it checks the four points in a diamond pattern
          around the unit's center.) The function returns true if it encounters no blocked tiles and false otherwise
        :param check_point:
        :param current_point_next:
        :return:
        """

        """

        """
    def walkable(self, a, b):
        print("a, b", a, b)
        x_a, y_a = a
        x_b, y_b = b
        x_max = max(x_a, x_b)
        y_max = max(y_a, y_b)
        print("x max und y max", x_max, y_max)
        while x_a != x_b and y_a != y_b:
            x_flag = y_flag = True

            if x_a != x_b and y_a != y_b:

                while x_a != x_b and y_a != y_b:

                    if x_max > x_a and x_flag:
                        x_a += 1

                    else:
                        x_flag = False
                        x_a -= 1

                    if y_max > y_a and y_flag:
                        y_a += 1

                    else:
                        y_flag = False
                        print("first 1 xa ya xb yb", x_a, y_a, x_b, y_b)
                        y_a -= 1
                    if self.field[[x_a],[y_a]] == 1:
                        return False

            x_flag = y_flag = True

            if x_a != x_b and y_a == y_b:
                print("second xa != xb")

                while x_a != x_b:
                    print("entered while")
                    if x_max > x_a and x_flag:
                        print("second 2 xa ya xb yb", x_a, y_a, x_b, y_b)

                        while x_a < x_b:
                            x_a += 1
                            print("second 3 xa ya xb yb", x_a, y_a, x_b, y_b)
                            if self.field[[x_a], [y_a]] == 1:
                                return False

                        while x_a > x_b:
                            x_a -= 1
                            print("second 3 xa ya xb yb", x_a, y_a, x_b, y_b)
                            if self.field[[x_a], [y_a]] == 1:
                                return False

                    else:
                        x_flag = False
                        print("second 4 xa ya xb yb", x_a, y_a, x_b, y_b)

                        while x_a > x_b:
                            x_a -= 1
                            print("second 5 xa ya xb yb", x_a, y_a, x_b, y_b)
                            if self.field[[x_a], [y_a]] == 1:
                                print("second 2 xa ya xb yb", x_a, y_a, x_b, y_b)
                                return False

            y_flag = True

            if x_a == x_b and y_a != y_b:
                print("third ya != yb")
                while y_a != y_b:

                    if y_max > y_a and y_flag:

                        while y_a < y_b:
                            y_a += 1

                            if self.field[[x_a], [y_a]] == 1:
                                print("third 1 xa ya xb yb", x_a, y_a, x_b, y_b)
                                return False

                        while y_a > y_b:
                            y_a -= 1
                            if self.field[[x_a], [y_a]] == 1:
                                print("third 2 xa ya xb yb", x_a, y_a, x_b, y_b)
                                return False
                    else:
                        y_flag = False

                        while y_a > y_b:
                            y_a -= 1
                            print("third 2 xa ya xb yb", x_a,y_a, x_b, y_b)
                            if self.field[[x_a], [y_a]] == 1:
                                return False
        return True

    #calculates next step and returns response values for server in shape of an 2D force vector.
    def go_for_target(self, ball_pos, radius):
        print("reached go for target")
        """

        :param ball_pos:
        :param radius:
        :return:
        """
        x_pos, y_pos = ball_pos
        x_pos_int, y_pos_int = int(x_pos), int(y_pos)
        start = (x_pos_int, y_pos_int)
        print("start", start)
        r = radius

        #TODO replacing kdtree with calc of nearest target
        tree = spatial.KDTree(self.targets)

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
        c = (x - r, y)
        d = (x + r, y)
        # c <= start <= d
        e = (x, y - r)
        f = (x, y + r)
        # e <= start <= f
        g = (x - r, y + r)
        g_x, g_y = g
        h = (x + r, y - r)
        h_x, h_y = h
        # g <= start <= h
        start_x, start_y = start

        #Checks every edgecase of a target collision. Adds prior collected target from
        #tar_onhold and removes collected target, from targets.
        if start == goal or nxt_mv == goal or c <= start <= d and e <= start <= f or g_x <= start_x <= h_x and h_y <= start_y <= g_y and a_x <= start_x <= b_x and a_y <= start_y <= b_y:
            self.targets.pop(index)

            if self.tar_onhold != 0:
                self.targets.append(self.tar_onhold)

            self.tar_onhold = goal
            return 0, 0
######################################################################################################################
        #If no target was hit, increase counter to calculate astar
        else:
            self.counter += 1

            #And if counter to calculate astar has reached max, calculate path via astar and reset counter. Otherwise, path
            #stays current path
            if self.counter == 20:
                self.path = self.astar(self.field, start, goal)
                print("path", self.path)
                self.counter = 0
                #path = self.path

            #else:
                #path = self.path
            step = 1

            #If path is empty, set path_len to zero. Otherwise path_len ist path length
            if self.path == False:
                path_len = self.path
            else:
                path_len = self.path.__len__()

            #If path is longer than next step, get next element from path as long as next_mv is unequal to start position.
            #And if path length ist < 30, set counter to 19.
            if path_len >= step:
                nxt_mv_ok = False

                while (not nxt_mv_ok):
                    #nxt_mv = self.path.pop() #TODO replacing pop() operation by a more complex function

                    """
                                 #Pseudocode
                                 #for smoothing algorithm.The smoothing algorithm simply checks from waypoint to waypoint along the path, trying to eliminate intermediate waypoints when possible.

                                checkPoint = starting point of path
                                currentPoint = next point in path
                                while (currentPoint->next != NULL)
                                    if Walkable(checkPoint, currentPoint->next)
                                         // Make a straight path between those points:
                                temp = currentPoint
                                currentPoint = currentPoint->next
                                delete temp from the path
                                else
                                checkPoint = currentPoint
                                currentPoint = currentPoint->next
                    """

                    cond = self.path.__len__()
                    while cond != 3:
                        print("condition", cond)
                        print("parth", self.path)
                        check_point = self.path[-1]
                        current_point = self.path[-2]
                        current_point_next = self.path[-3]
                        print("checkpoin, current point. current next", check_point, current_point, current_point_next)
                        print("length of parth", self.path.__len__())


                        if self.walkable(check_point, current_point_next):

                            #current_point = current_point_next
                            print("after walkable true")

                            x = self.path.pop(-2)
                            current_point_next = self.path[-3]
                            current_point = self.path[-2]
                            cond -= 1
                            print("smothing pop", x)
                        else:
                            cond = 3
                            if start == current_point:
                                self.path = self.astar(self.field, start, goal)
                            print("cont bottom", cond)
                            #print("nxt mv = current pint", current_point)
                        nxt_mv = current_point


                    if (nxt_mv != start):
                        nxt_mv_ok = True

                if (self.path.__len__() <= 30):
                    self.counter = 19
#######################################################################################################################
            #Otherwise if path lenght is 0, return no force(0, 0)
            elif path_len == False:
                return 0, 0

            self.nxt_mv = nxt_mv
            x, y = self.resp_normalized(start, nxt_mv)
            print("response", x, y, self.nxt_mv)
            return x, y


