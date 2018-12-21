import itertools
import math
from heapq import *

"""
mir faellt grade nicht weiter ein, was ich noch von eimem Pfad wollen koennte.
"""

#[Point(512,691), Point(511,690), Point(511,521), Point(462,472), Point(462,471), Point(462,470), Point(462,469), Point(462,468), Point(462,467), Point(462,466), Point(462,465), Point(462,464), Point(462,463), Point(462,462), Point(462,461), Point(462,460), Point(462,459), Point(462,458), Point(462,457), Point(462,456), Point(462,455), Point(462,454), Point(462,453), Point(462,452), Point(462,451), Point(462,450), Point(462,449), Point(462,448), Point(462,447), Point(462,446), Point(462,445), Point(462,444), Point(462,443), Point(462,442), Point(462,441), Point(462,440), Point(462,439), Point(462,438), Point(462,437), Point(462,436), Point(462,435), Point(462,434), Point(462,433), Point(462,432), Point(462,431), Point(462,430), Point(462,429), Point(462,428), Point(462,427), Point(462,426), Point(462,425), Point(462,424), Point(462,423), Point(462,422), Point(462,421), Point(462,420), Point(462,419), Point(462,418), Point(463,417), Point(464,417), Point(465,417), Point(466,417), Point(467,417), Point(468,417), Point(469,417), Point(470,417), Point(471,417), Point(472,417), Point(473,417), Point(474,417), Point(475,417), Point(476,417), Point(477,417), Point(478,417), Point(479,417), Point(480,417), Point(481,417), Point(482,417), Point(483,417), Point(484,417), Point(485,417), Point(486,417), Point(487,417), Point(488,417), Point(489,417), Point(490,417), Point(491,417), Point(492,417), Point(493,417), Point(494,417), Point(495,417), Point(496,417), Point(497,417), Point(498,417), Point(499,417), Point(500,417), Point(501,417), Point(502,417), Point(503,417), Point(504,417), Point(505,417), Point(506,417), Point(507,417), Point(508,417), Point(509,417), Point(510,417), Point(511,417), Point(512,416), Point(512,415), Point(512,414), Point(512,413), Point(512,412), Point(512,411), Point(512,410), Point(512,409), Point(512,408), Point(512,407), Point(512,406), Point(512,405), Point(512,404), Point(512,403), Point(512,402), Point(512,401), Point(512,400), Point(512,399), Point(512,398), Point(512,397), Point(512,396), Point(512,395), Point(512,394), Point(512,393), Point(512,392), Point(512,391), Point(512,390), Point(512,389), Point(512,388), Point(512,387), Point(512,386), Point(512,385)]
#[Point(512,691), Point(511,690), Point(511,521), Point(462,472), Point(462,418), Point(463,417), Point(511,417), Point(512,416), Point(512,385)]
#[Point(512,691), Point(462,472), Point(463,417), Point(512,385)]

def test():
    import numpy as np
    peter = Path([(1,1),(1,2),(1,3),(1,4),(2,4),(3,4)])
    anton = Path([(3,1),(3,2),(4,3),(4,4),(4,5),(4,6),(4,7),(5,7),(5,6)])
    print("Peter: ",peter)
    print("Anton: ",anton)
    star = StarPath([(0,0),(10,10),(10,0),(5,5)])
    star.paths.append(anton)
    star.paths.append(peter)
    star.field = np.zeros([11, 11], dtype=object)
    star.field[[5],[5]] = 1
    PointA = Point(None, (0,0))
    PointB = Point(None, (10,10))
    PointC = Point(None, (10,3))
    print(walkable(star.field, PointA, PointB))
    print(walkable(star.field, PointA, PointC))
    print(walkable(star.field, PointB, PointA))

    import pdb
    pdb.Pdb().set_trace()
    nxt_mv = peter.points[0]
    ball_pos = Point(None, (1,3))
    nxt_mv = nxt_mv.next()
    while nxt_mv is not None and ball_pos.dist(peter.getLastPoint()) <= nxt_mv.dist(peter.getLastPoint()):
        nxt_mv = nxt_mv.next()
    print("Shortest Path: ",star.getShortestPath())
    import pdb
    pdb.Pdb().set_trace()
    peter.simplifyPath()
    peter.smoothifyPath(star.field)

def astern(array, start, goal):
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

# linear interpolation
def walkable(array, pointA, pointB):
    #def lipo(start, end, perc):
    #    return start + perc * (end - start)
    dPoint = pointB - pointA
    dx, dy = dPoint.getXY()
    max = abs(dx if abs(dx) > abs(dy) else dy)
    for i in range(max):
        y = (i/max * dy)
        x = (i/max * dx)
        x, y = (pointA + Point(None, (x,y))).getXY()
        if array[[x], [y]]:
            return False
    return True

class StarPath:
    def __init__(self, targets, field=None):
        self.field = field
        self.targets = targets
        self.paths = []
        if field is not None:
            self.calcPaths()
            self.simplifyPaths()
            self.smoothPaths()

    def calcPaths(self):
        combinations = itertools.combinations(self.targets, 2)
        for combination in combinations:
            start, target = combination
            self.paths.append(Path(astern(self.field, start, target)))

    def simplifyPaths(self):
        for path in self.paths:
            path.simplifyPath()

    def smoothPaths(self):
        for path in self.paths:
            path.smoothifyPath(self.field)

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

    def findPathWithEnd(self, end, range=1):
        l = []
        for path in self.paths:
            if path.getLastPoint().inRange(range, end):
                l.append(path.getLastPoint(self))
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
        self.smoothPath = None

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
                simplePoints.append(start.getXY())
            lastdiff = diff
        simplePoints.append(self.points[len(self.points)-1].getXY())
        self.simplePath = Path(simplePoints)

    # use only after simplifyPath has been called
    def smoothifyPath(self, field):
        smoothPoints = []
        point = 0
        smoothPoints.append(self.simplePath.points[0].getXY())
        while point < len(self.simplePath.points)-1:
            start = self.simplePath.points[point]
            p = start.next()
            while p is not None:
                if walkable(field, start, p):
                    last_walkable = p
                    p = p.next()
                else:
                    p = None
            smoothPoints.append(last_walkable.getXY())
            point = self.simplePath.points.index(last_walkable)
        self.smoothPath = Path(smoothPoints)

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
