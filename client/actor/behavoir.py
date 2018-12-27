from client.actor import starpath as sP
#from actor import starpath as sP

class Behavior(object):
    def __init__(self, starpath, field, radius):
        self.radius = radius
        self.starpath = starpath
        self.field = field
        self.nxt_mv = None
        self.path = None
        self.reverse = False
        self.name = "No name"

    def slowDown(self, ball_pos, ball_force):
        fx, fy = ball_force.getXY()
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

    def update(self, ball_pos, ball_force):
        # 35 -> Target size!
        # reached nxt_mv? Fetch the new nxt_mv and slowDown becauhse in smoothPath/simplepath, every point is a corner
        # if there is no next mv, reverse direction!
        if ball_pos.inRange(self.radius + 10, self.nxt_mv):
            if not self.reverse:
                self.nxt_mv = self.nxt_mv.next()
                if self.nxt_mv is None:
                    self.reverse = not self.reverse
                    self.nxt_mv = self.path.getLastPoint()
                else:
                    return self.slowDown(ball_pos, ball_force)
            else:
                self.nxt_mv = self.nxt_mv.prior()
                if self.nxt_mv is None:
                    self.reverse = not self.reverse
                    self.nxt_mv = self.path.getFirstPoint()
                else:
                    return self.slowDown(ball_pos, ball_force)

        # if the ball misses a mv but the ball is still on the path: jump to next mv
        # TODO ADD CHECK IF OBSTACLE IS IN THE WAY
        if not self.reverse:
            while self.nxt_mv is not None and ball_pos.dist(self.path.getLastPoint()) < self.nxt_mv.dist(
                    self.path.getLastPoint()):
                self.nxt_mv = self.nxt_mv.next()
        else:
            while self.nxt_mv is not None and ball_pos.dist(self.path.getFirstPoint()) < self.nxt_mv.dist(
                    self.path.getFirstPoint()):
                self.nxt_mv = self.nxt_mv.prior()

        # if the ball lost its path but the target is in clear sight:
        if sP.walkable(self.field, ball_pos,
                       self.path.getFirstPoint() if self.reverse else self.path.getLastPoint()):
            self.nxt_mv = self.path.getFirstPoint() if self.reverse else self.path.getLastPoint()

        # if near target, slowdown!
        fx, fy = ball_force.getXY()
        if ball_pos.inRange(140, self.path.getFirstPoint() if self.reverse else self.path.getLastPoint()) and (
                abs(fx) > 1 or abs(fy) > 1):
            return self.slowDown(ball_pos, ball_force)

        return (self.nxt_mv - ball_pos).norm()

    def __str__():
        return self.name



#bewegt sich ueber das ganze Spielfeld und probiert verschiedene Pfade aus.
# -> alle Pfade auf einen Stack und poppen bis der Stack leer ist, dann wieder von vorne
#in anderer Reihenfolge
class explorer(Behavior):
    def __init__(self, starpath, field, radius):
        super(explorer, self).__init__(starpath, field, radius)
        self.nxt_mv = None
        self.path = None
        self.reverse = False
        self.name = "No name"


#nimmt immer wieder den am vielversprechendsten Pfad. Dieses kann ein besonders kurzer Pfad sein
#oder ein besonders leicht abzufahrender Pfad, da jedes obstacle collision minuspunkte bedeutet
# und der Ball schwer zu navigieren ist.
# -> nimmt den kürzesten Pfad und bleibt auf diesem
class bestPerformance(Behavior):

#nimmt keine Ruecksicht auf den Gegenspieler, macht nur sein eigenes
#Ding(evtl einfach default behavior?)
class ignorant(Behavior):

#ist gaenzlich passiv. sollte jedoch input liefern falls der Gegenspieler nichts mehr
# macht, damit der Spieler nicht denk dass niemand mit spielt.
class follower(Behavior):


#Mischung aus explorer, best performance und follower. Sollte saemtliche Pfade ausprobieren und
# dabei 'lernen' den daraus resultierenden besten Pfad immer wieder zu benutzen. Beim
# exploren versucht er auch heraus zu finden , wo die Hindernisse beim Gegenspieler liegen.
#learning-following-explorer
class leFollowEx(Behavior):


#Mischung aus explorer, best performance und ignorant. Sollte saemtliche Pfade ausprobieren und
#dabei 'lernen' den daraus resultierenden besten Pfad immer wieder zu benutzen. Beim
#exploren versucht er nicht heraus zu finden wo die Hindernisse beim Gegenspieler
#liegen, sondern findet nur seinen optimalen Pfad unabhaengig vom Gegenueber.
#learning - ignorant - explorer
class leIgnoEx(Behavior):


# nimmt immer wieder den am vielversprechendsten Pfad. Dieses kann ein besonders
# kurzer Pfad sein oder ein besonders leicht abzufahrender Pfad, da jedes obstacle
# collision minuspunkte bedeutet und der Ball schwer zu navigieren ist. Er ignoriert
# dabei, dass er noch einen Gegenspieler hat.
#best perfomance-ignorant
class bestIgno(Behavior):

#nimmt immer wieder den am vielversprechendsten Pfad. Dieses kann ein besonders
#kurzer Pfad sein oder ein besonders leicht abzufahrender Pfad, da jedes obstacle
#collision minuspunkte bedeutet und der Ball schwer zu navigieren ist. Er bemerkt
#wenn auf seinem Idealen Pfad unsichtbare Hindernisse liegen und aendert ihn gebenen
#falls. Wenn ihn der gegenspieler gaenzlich von seinem Erfolgspfad abbringt, folgt
#er ihm bis er wieder in die Naehe von seinem Erfolgspfad kommt.
#best perfomance-follower
class bestFollow(Behavior):