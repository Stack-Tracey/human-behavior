import numpy as np
import client.actor.trialState as tS
#from scipy import spatial

class Search:
    def __init__(self, field, targets):
        self.field = field
        self.targets = targets
        self.star = tS.StarPath(self.targets, self.field)
        self.tar_onhold = 0

        self.nxt_mv = None
        self.path = None
        self.behavoir = "default"
        self.reverse = False


    """#returns force on ball normalized to [-1, 1]
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

    """
     samples points along a line from point A= checkpoint to point B = current_point_next at a certain granularity
     (typically we use one-fifth of a tile width), checking at each point whether the unit overlaps
     any neighboring blocked tile. (Using the width of the unit, it checks the four points in a diamond pattern
      around the unit's center.) The function returns true if it encounters no blocked tiles and false otherwise
    :param check_point:
    :param current_point_next:
    :return:
    """

    def walkable(self, a, b):
        print("walkable : a, b", a, b, "############################################################WALKABLE")

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
                        y_a -= 1
                    if self.field[[x_a],[y_a]] == 1:
                        return False
            print(" a!=b", x_a, y_a, x_b, y_b)

            x_flag = y_flag = True

            if x_a != x_b and y_a == y_b:

                while x_a != x_b:

                    if x_max > x_a and x_flag:

                        while x_a < x_b:
                            x_a += 1

                            if self.field[[x_a], [y_a]] == 1:
                                return False

                        while x_a > x_b:
                            x_a -= 1

                            if self.field[[x_a], [y_a]] == 1:
                                return False

                    else:
                        x_flag = False

                        while x_a > x_b:
                            x_a -= 1
                            if self.field[[x_a], [y_a]] == 1:
                                return False
            print(" ax!=bx ay==by", x_a, y_a, x_b, y_b)
            y_flag = True

            if x_a == x_b and y_a != y_b:

                while y_a != y_b:
                    print("ax == bx ay!=by", x_a, y_a, x_b, y_b)

                    if y_max > y_a and y_flag:

                        while y_a < y_b:
                            y_a += 1
                            print("ax == bx ay!=by", x_a, y_a, x_b, y_b)

                            if self.field[[x_a], [y_a]] == 1:
                                return False

                        while y_a > y_b:
                            y_a -= 1
                            print("ax == bx ay!=by", x_a, y_a, x_b, y_b)

                            if self.field[[x_a], [y_a]] == 1:
                                return False
                    else:
                        y_flag = False

                        while y_a > y_b:
                            y_a -= 1

                            if self.field[[x_a], [y_a]] == 1:
                                return False

                print("ax == bx ay!=by", x_a, y_a, x_b, y_b)
        return True

    """
    #calculates next step and returns response values for server in shape of an 2D force vector.
    def go_for_target(self, ball_pos, radius):
        print("############################################################GO FOR TARGET")

        x_pos, y_pos = ball_pos
        x_pos_int, y_pos_int = int(x_pos), int(y_pos)
        start = (x_pos_int, y_pos_int)
        print("start", start)
        r = radius

        #TODO replacing kdtree with calc of nearest target
        tree = spatial.KDTree(self.targets)

        index = tree.query([start])[1][0]
        goal = self.targets[index]
        print("goal", goal)

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
        nxt_x, nxt_y = self.nxt_mv
        print("next mv", self.nxt_mv)

        if ((((nxt_x + 1),(nxt_y + 1)) == goal or ((nxt_x - 1),(nxt_y - 1)) == goal)) and start != goal and start != self.nxt_mv:
            while start != goal and start != self.nxt_mv:
                x, y = self.resp_normalized(start, self.nxt_mv)
                print("response1", x, y, self.nxt_mv)
                return x, y

        #Checks every edgecase of a target collision. Adds prior collected target from
        #tar_onhold and removes collected target, from targets.
        elif start == goal or ((nxt_x + 1),(nxt_y + 1)) == goal or ((nxt_x - 1),(nxt_y - 1)) == goal or c <= start <= d and e <= start <= f or g_x <= start_x <= h_x and h_y <= start_y <= g_y and a_x <= start_x <= b_x and a_y <= start_y <= b_y:
            self.targets.pop(index)

            if self.tar_onhold != 0:
                self.targets.append(self.tar_onhold)

            self.tar_onhold = goal
            return 0, 0
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

            if self.nxt_mv == goal:
                nxt_mv_ok = True

            #If path is longer than next step, get next element from path as long as next_mv is unequal to start position.
            #And if path length ist < 30, set counter to 19.
            if path_len >= step:
                nxt_mv_ok = False
######################################################################################################################
                current_point = []
                while (not nxt_mv_ok):
                    #nxt_mv = self.path.pop() #TODO replacing pop() operation by a more complex function

                    self.cond = self.path.__len__()
                    while self.cond != 3:
                        print("condition", self.cond)
                        print("parth", self.path)
                        check_point = self.path[-1]
                        current_point = self.path[-2]
                        current_point_next = self.path[-3]

                        print("checkpoin, current point. current next", check_point, current_point, current_point_next)
                        print("length of parth", self.path.__len__())

                        while self.walkable(check_point, current_point_next) and self.cond != 3:

                            x = self.path.pop(-2)
                            current_point_next = self.path[-3]
                            current_point = self.path[-2]
                            self.cond -= 1
                            print("smothing pop", x)

                        self.cond = 3
                        print("walkable false")
                        if start == current_point:
                            self.path = self.astar(self.field, start, goal)
                        self.nxt_mv = current_point
                        print("nxt mv 2", self.nxt_mv)
#######################################################################################################################
                    self.nxt_mv = current_point
                    if self.nxt_mv != start:
                        nxt_mv_ok = True

                if self.path.__len__() <= 30:
                    self.counter = 19

            #Otherwise if path lenght is 0, return no force(0, 0)
            elif path_len == False:
                return 0, 0

            #self.nxt_mv = nxt_mv
            x, y = self.resp_normalized(start, self.nxt_mv)
            print("response", x, y, self.nxt_mv)
            return x, y
    """
    def go_for_target(self, ball_pos, ball_force, radius):
        ball_pos = tS.Point(None, ball_pos)
        fx, fy = ball_force

        # Default behavoir is an example of the new StarPath-class
        # it follows a pre-calculated astar path.
        # if the end is reached, it revers back again
        if self.behavoir == "default":
            def slowDown():
                x, y = (self.nxt_mv - ball_pos).norm()
                if fx > 1:
                    x = -0.35
                if fx < -1:
                    x = 0.35
                if fy > 1:
                    y = -0.35
                if fy < -1:
                    y = 0.35
                return (x, y)

            if self.path is None:
                #self.path = self.star.getShortestPath().smoothPath # works like a charm
                #self.path = self.star.getLongestPath() # looks weird but works, give it a bit time
                self.path = self.star.paths[1].smoothPath # looks a bit less weird but works, give it a bit time
                #import pdb
                #pdb.Pdb().set_trace()
                #self.path = self.star.getShortestPath().getSimplePath()
                self.nxt_mv = self.path.getLastPoint()
                self.reverse = False
                return (self.nxt_mv - ball_pos).norm()

            # 35 -> Target size!
            # reached nxt_mv? Fetch the new nxt_mv and slowDown because in smoothPath/simplepath, every point is a corner
            # if there is no next mv, reverse direction!
            if ball_pos.inRange(radius+10,self.nxt_mv):
                if not self.reverse:
                    self.nxt_mv = self.nxt_mv.next()
                    if self.nxt_mv is None:
                        self.reverse = not self.reverse
                        self.nxt_mv = self.path.getLastPoint()
                    else:
                        slowDown()
                else:
                    self.nxt_mv = self.nxt_mv.prior()
                    if self.nxt_mv is None:
                        self.reverse = not self.reverse
                        self.nxt_mv = self.path.getFirstPoint()
                    else:
                        slowDown()

            # if the ball misses a mv but the ball is still on the path: jump to next mv
            # TODO ADD CHECK IF OBSTACLE IS IN THE WAY
            if not self.reverse:
                while self.nxt_mv is not None and ball_pos.dist(self.path.getLastPoint()) < self.nxt_mv.dist(self.path.getLastPoint()):
                    self.nxt_mv = self.nxt_mv.next()
            else:
                while self.nxt_mv is not None and ball_pos.dist(self.path.getFirstPoint()) < self.nxt_mv.dist(self.path.getFirstPoint()):
                    self.nxt_mv = self.nxt_mv.prior()

            # if the ball lost its path but the target is in clear sight:
            if tS.walkable(self.field, ball_pos, self.path.getFirstPoint() if self.reverse else self.path.getLastPoint()):
                self.nxt_mv = self.path.getFirstPoint() if self.reverse else self.path.getLastPoint()

            # if near target, slowdown!
            if ball_pos.inRange(140, self.path.getFirstPoint() if self.reverse else self.path.getLastPoint()) and (abs(fx) > 1 or abs(fy) > 1):
                slowDown()

            return (self.nxt_mv - ball_pos).norm()
        """
        if self.behavoir == "explorer":
            bewegt sich über das ganze Spielfeld und probiert verschiedene Pfade aus.
            
        if self.behavoir == "best performance":
            nimmt immer wieder den am vielversprechendsten Pfad. Dieses kann ein besonders
            kurzer Pfad sein oder ein besonders leicht abzufahrender Pfad, da jedes obstacle 
            collision minuspunkte bedeutet und der Ball schwer zu navigieren ist. 
            
        if self.behavoir == "ignorant":
            nimmt keine Rücksicht auf den gegenspieler, macht nur sein eigenes Ding(evtl einfach
            default behavior?)
            
        if self.behavoir == "follower":
            ist gänzlich passiv. sollte jedoch input liefern falls der Gegenspieler nichts mehr 
            macht, damit der Spieler nicht denk dass niemand mit spielt.
            
     Das hier sind die Endtypen die sich aus den anderen zusammensetzen
            
        if self.behavoir == "learning-following-explorer": 
            Mischung aus explorer, best performance und follower. Sollte sämtliche Pfade ausprobieren und
            dabei 'lernen' den daraus resultierenden besten Pfad immer wieder zu benutzen. Beim
            exploren versucht er auch heraus zu finden , wo die Hindernisse beim Gegenspieler 
            liegen. 
            
        if self.behavior == "learning-ignorant-explorer":
            Mischung aus explorer, best performance und ignorant. Sollte sämtliche Pfade ausprobieren und
            dabei 'lernen' den daraus resultierenden besten Pfad immer wieder zu benutzen. Beim
            exploren versucht er nicht heraus zu finden wo die Hindernisse beim Gegenspieler
            liegen, sondern findet nur seinen optimalen Pfad unabhängig vom Gegenüber.
            
        if self.behavior == "best perfomance-ignorant":
            nimmt immer wieder den am vielversprechendsten Pfad. Dieses kann ein besonders
            kurzer Pfad sein oder ein besonders leicht abzufahrender Pfad, da jedes obstacle 
            collision minuspunkte bedeutet und der Ball schwer zu navigieren ist. Er ignoriert
            dabei, dass er noch einen Gegenspieler hat.
                 
        
        if self.behavior == "best perfomance-follower": 
            nimmt immer wieder den am vielversprechendsten Pfad. Dieses kann ein besonders
            kurzer Pfad sein oder ein besonders leicht abzufahrender Pfad, da jedes obstacle 
            collision minuspunkte bedeutet und der Ball schwer zu navigieren ist. Er bemerkt
            wenn auf seinem Idealen Pfad unsichtbare Hindernisse liegen und ändert ihn gebenen
            falls. Wenn ihn der gegenspieler gänzlich von seinem Erfolgspfad abbringt, folgt
            er ihm bis er wieder in die Nähe von seinem Erfolgspfad kommt.
        
        """
