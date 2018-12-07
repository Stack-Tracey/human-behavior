import itertools
import math
from client.actor import nodes
from heapq import *

def test():
    peter = Path([(1,1),(1,2),(1,3),(1,4),(2,4),(3,4)])
    anton = Path([(3,1),(3,2),(4,3),(4,4),(4,5),(4,6),(4,7),(5,7),(5,6)])
    print("Peter: ",peter)
    print("Anton: ",anton)
    star = StarPath([(0,0),(10,10),(10,0),(5,5)],(0,0))
    star.paths.append(anton)
    star.paths.append(peter)
    print("Shortest Path: ",star.getShortestPath())
    import pdb
    pdb.Pdb().set_trace()

class StarPath:
    def __init__(self, targets, start, field=None):
        self.field = field
        self.targets = targets
        self.start = start
        self.paths = []
        if field is not None:
            self.calcPaths()
            self.simplifyPaths()

    def astern(self, array, start, goal):
        # L1-norm manhattan distance as heuristik for astar
        def heuristic(a, b):
            return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

        print("calculated A*")
        open_heap = []
        came_from = {}
        close_set = set()
        gscore = {start: 0}
        hscore = {start: heuristic(start, goal)}
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
                tent_g_score = gscore[current] + heuristic(current, neighbor)
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
                    hscore[neighbor] = tent_g_score + heuristic(neighbor, goal)
                    heappush(open_heap, (hscore[neighbor], neighbor))

        return False

    def calcPaths(self):
        combinations = itertools.combinations(self.targets, 2)
        for combination in combinations:
            start, target = combination
            self.paths.append(Path(self.astern(self.field, start, target)))

    def simplifyPaths(self):
        for path in self.paths:
            path.simplifyPath()

    # this function returns the shortest path
    def getShortestPath(self):
        min = self.paths[0]
        for each in  self.paths:
            if each.getLength() < min.getLength():
                min = each
        return min

    def getLongestPath(self):
        max = self.paths[0]
        for each in self.paths:
            if each.getLength() > max.getLength():
                max = each
        return max

    def getNearPoint(self, pos):
        min = self.paths[0].getPoints()[0]
        mindist = pos.dist(min)
        for path in self.paths:
            for point in path.getPoints():
                thisdist = pos.dist(point)
                if thisdist < mindist:
                    min = point
                    mindist = thisdist
        return min

    def getNearPath(self, pos):
        return self.getNearPoint(pos).getPath()

    def getNearPointAsXY(self, pos):
        return self.getNearPoint(pos).getXY()

    def getNearSimplePoint(self, pos):
        min = self.paths[0].getSimplePath().getPoints()[0]
        mindist = pos.dist(min)
        for path in self.paths:
            for point in path.getSimplePath().getPoints():
                thisdist = pos.dist(point)
                if thisdist < mindist:
                    min = point
                    mindist = thisdist
        return min

    def getNearSimplePointAsXY(self, pos):
        return self.getNearSimplePoint(pos).getXY()

    def findPathWithStart(self, start, range=1):
        l = []
        for path in self.paths:
            if path.getFirstPoint().inRange(range, start):
                l.append(path.getFirstPoint(self))
        return l


class Path:
    def __init__(self, points):
        def toPoints(p):
            a = []
            for i in p:
                if isinstance(i, Point):
                    a.append(i)
                else:
                    a.append(Point(self, i))
            return a
        self.points = toPoints(points)
        self.simplePath = None

    def getLength(self):
        return len(self.points)
        # stuff

    def getPoints(self):
        return self.points

    def simplifyPath(self):
        lastdiff = (0,0)
        simplePoints = []
        for point in range(len(self.points)-1):
            start = self.points[point]
            next = self.points[point+1]
            diff = (next - start).getXY()
            if diff != lastdiff:
                simplePoints.append(start)
            lastdiff = diff
        simplePoints.append(self.points[len(self.points)-1])
        self.simplePath = Path(simplePoints)

    def getSimplePath(self):
        return self.simplePath

    def getFirstPoint(self):
        return self.points[0]

    def getLastPoint(self):
        return self.points[len(self.points)-1]

    def __str__(self):
        return "Path(%d)" % self.getLength()

    def __repr__(self):
        return self.__str__()


class Point:
    def __init__(self, path, pos):
        self.path = path
        self.pos = pos

    def getPath(self):
        return self.path

    def getXY(self):
        return self.pos

    def dist(self, other):
        diff = self - other
        x, y = diff.getXY()
        return math.sqrt(x*x + y*y)

    def inRange(self, range, other):
        return self.dist(other) <= range

    def next(self):
        if self.path is None:
            return None
        i = self.path.points.index(self)
        if i == self.path.getLength()-1:
            return None
        return self.path.points[i+1]

    def prior(self):
        if self.path is None:
            return None
        i = self.path.points.index(self)
        if i == 0:
            return None
        return self.path.points[i + -1]

    def norm(self):
        if self.pos == (0, 0):
            return 0, 0
        x_r, y_r = self.pos
        m = math.sqrt(pow(x_r, 2) + pow(y_r, 2))

        x_rn = (1 / m) * x_r
        y_rn = (1 / m) * y_r

        return x_rn, y_rn

    def __sub__(self, other):
        x, y = other.getXY()
        sx, sy = self.pos
        return Point(None, (sx-x, sy-y))

    def __add__(self, other):
        x, y = other.getXY()
        sx, sy = self.pos
        return Point(None, (sx+x, sy+y))

    def __eq__(self, other):
        return other.getXY() == self.pos


    def __str__(self):
        return "Point(%d,%d)" % self.pos

    def __repr__(self):
        return self.__str__()


class TrialState:
    def __init__(self, obs_x, obs_y, obs_z, obs_x_size, obs_y_size, obs_z_size, obs_z_angle_deg, obs_slowdown_fac,
                  obs_visibility, obs_geometric_type, tar_x, tar_y, tar_z, tar_z_size, tar_radius, ball_x, ball_y,
                  ball_z, ball_radius, nr_of_targets, nr_of_obstacles):

        self.obs_x = obs_x
        self.obs_y = obs_y
        self.obs_z = obs_z
        self.obs_x_size = obs_x_size
        self.obs_y_size = obs_y_size
        self.obs_z_size = obs_z_size
        self.obs_z_angle_deg = obs_z_angle_deg
        self.obs_slowdown_fac = obs_slowdown_fac
        self.obs_visibility = obs_visibility
        self.obs_geometric_type = obs_geometric_type
        self.nr_of_obstacles = nr_of_obstacles

        self.tar_x = tar_x
        self.tar_y = tar_y
        self.tar_z = tar_z
        self.tar_z_size = tar_z_size
        self.tar_radius = tar_radius
        self.targets_tup = []
        self.nr_of_targets = nr_of_targets

        self.ball_x = ball_x
        self.ball_y = ball_y
        self.ball_z = ball_z
        self.ball_radius = ball_radius
        self.ball = (ball_x, ball_y)# ball_z, ball_radius

        #TODO handling of different behavior: adding param for 'perfectness' and include to seeing all obstacles
        #returns the positions of obstacles.
        #visible_fac_val = {1. visible for player one, 2. visible for player two, 3. visible for both}
        def get_obstacles(obs_x, obs_y, obs_z, obs_x_size, obs_y_size, obs_z_size, obs_z_angle_deg, obs_slowdown_fac, visibility, geometric_type):
            obstacles = []
            i = 0

            while i < nr_of_obstacles:
                x_val = obs_x[i]
                y_val = obs_y[i]
                z_val = obs_z[i]
                x_size_val = obs_x_size[i]
                y_size_val = obs_y_size[i]
                z_size_val = obs_z_size[i]
                angle_deg_val = obs_z_angle_deg[i]
                slowdown_fac_val = obs_slowdown_fac[i]
                visible_fac_val = visibility[i]
                geometric_type_val = geometric_type[i]

                if visible_fac_val == 1 or visible_fac_val == 3:
                    obs = [x_val, y_val, z_val, x_size_val, y_size_val, z_size_val, angle_deg_val, slowdown_fac_val, visible_fac_val, geometric_type_val]
                    obstacles.append(obs)

                i = i + 1
            print("obstacles, should be less than 9 elements: ", obstacles)
            return obstacles

        #returns the positions of targets.
        def get_targets(tar_x, tar_y, tar_z, tar_z_size, tar_radius, nr_of_targets):
            targets = []
            tar_buffer = []
            i = 0

            while i < nr_of_targets:
                x_val = tar_x[i]
                y_val = tar_y[i]
                z_val = tar_z[i]
                z_size_val = tar_z_size[i]
                radius_val = tar_radius
                nr_of_tar_val = nr_of_targets

                tar = [x_val, y_val, z_val, z_size_val, radius_val, nr_of_tar_val]
                tar_tup = (x_val, y_val)
                targets.append(tar)
                tar_buffer.append(tar_tup)

                i = i + 1

            self.targets_tup = sorted(tar_buffer)
            return targets

        self.obstacles = get_obstacles(self.obs_x, self.obs_y, self.obs_z, self.obs_x_size, self.obs_y_size,
                                       self.obs_z_size, self.obs_z_angle_deg, self.obs_slowdown_fac,
                                       self.obs_visibility, self.obs_geometric_type)
        self.targets = get_targets(tar_x, tar_y, tar_z, tar_z_size, tar_radius, nr_of_targets)
        self.nodes = nodes.Nodes(self.obstacles, self.targets, self.ball, self.ball_radius)
        print("reached self.nodes")
        #self.tar_nodes = self.nodes.tar_nodes
        self.obs_nodes = self.nodes.obstacles
        self.field_filled = self.nodes.field_filled







