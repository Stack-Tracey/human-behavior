from client.actor import starpath as sP
import random


# from actor import starpath as sP

class Behavior(object):
    def __init__(self, starpath, field, radius):
        self.radius = radius
        self.starpath = starpath
        self.field = field
        self.journey = None
        self.target = None
        self.nxt_mv = None
        self.name = "No name"

    def slowDown(self, ball_pos, ball_force):
        if ball_force.abs() > 1:
            x, y = ball_force.getXY()
            return (-0.5 * x, -0.5 * y)
        return (self.nxt_mv - ball_pos).norm()

    # returns a random target wich is not our last one
    def giveNewTarget(self, currentTarget, origin):
        target = list(currentTarget.journeys)
        if len(target) == 1 and origin in target:
            return target[0]
        if origin in target:
            target.remove(origin)
        return random.choice(target)

    def update(self, ball_pos, ball_force):
        if not isinstance(ball_pos, sP.Point):
            ball_pos = sP.Point(None, ball_pos)
        if not isinstance(ball_force, sP.Point):
            ball_force = sP.Point(None, ball_force)

        atTarget = self.starpath.getNearTarget(ball_pos)
        if self.target is None:
            self.target = next(iter(atTarget.journeys))
            self.journey = atTarget.journeys[self.target]
            self.nxt_mv = self.journey.smooth.getFirstPoint()

        # 35 -> Target size!
        # reached nxt_mv? Fetch the new nxt_mv and slowDown becauhse
        # in smoothPath/simplepath, every point is a corner
        # if there is no next mv, reverse direction!
        if ball_pos.inRange(self.radius + 10, self.nxt_mv):
            self.nxt_mv = self.nxt_mv.next()

            # there is no next move but we hit the last one(our destination)
            if self.nxt_mv is None:
                self.target = next(iter(atTarget.journeys))
                self.journey = atTarget.journeys[self.target]
                self.nxt_mv = self.journey.smooth.getFirstPoint()
            else:
                return self.slowDown(ball_pos, ball_force)

        return (self.nxt_mv - ball_pos).norm()

    def __str__():
        return self.name


# bewegt sich ueber das ganze Spielfeld und probiert verschiedene Pfade aus.
# -> alle Pfade auf einen Stack und poppen bis der Stack leer ist, dann wieder von vorne
# in anderer Reihenfolge
class Explorer(Behavior):
    def __init__(self, starpath, field, radius):
        super(Explorer, self).__init__(starpath, field, radius)
        self.name = "Explorer"
        self.origin = None

    def update(self, ball_pos, ball_force):
        if type(ball_pos) != sP.Point:
            ball_pos = sP.Point(None, ball_pos)
        if type(ball_force) != sP.Point:
            ball_force = sP.Point(None, ball_force)

        atTarget = self.starpath.getNearTarget(ball_pos)
        if self.target is None:
            self.target = next(iter(atTarget.journeys))
            self.journey = atTarget.journeys[self.target]
            self.origin = atTarget
            self.nxt_mv = self.journey.smooth.getFirstPoint()

        # 35 -> Target size!
        # reached nxt_mv? Fetch the new nxt_mv and slowDown becauhse
        # in smoothPath/simplepath, every point is a corner
        # if there is no next mv, reverse direction!
        if ball_pos.inRange(self.radius + 10, self.nxt_mv):
            self.nxt_mv = self.nxt_mv.next()

            # there is no next move but we hit the last one(our destination)
            if self.nxt_mv is None:
                self.target = self.giveNewTarget(atTarget, self.origin)
                self.journey = atTarget.journeys[self.target]
                self.origin = atTarget
                self.nxt_mv = self.journey.smooth.getFirstPoint()
            else:
                return self.slowDown(ball_pos, ball_force)

        return (self.nxt_mv - ball_pos).norm()


# Mischung aus explorer, best performance und follower. Sollte saemtliche Pfade ausprobieren und
# dabei 'lernen' den daraus resultierenden besten Pfad immer wieder zu benutzen. Beim
# exploren versucht er auch heraus zu finden , wo die Hindernisse beim Gegenspieler liegen.
# learning-following-explorer
# class FollowEx(Behavior):


# Mischung aus explorer, best performance und ignorant. Sollte saemtliche Pfade ausprobieren und
# dabei 'lernen' den daraus resultierenden besten Pfad immer wieder zu benutzen. Beim
# exploren versucht er nicht heraus zu finden wo die Hindernisse beim Gegenspieler
# liegen, sondern findet nur seinen optimalen Pfad unabhaengig vom Gegenueber.
# learning - ignorant - explorer

# 1.) Mal rumprobieren
# 2.) Den Besten weg nehemen und endlos punkte sammeln
class IgnoEx(Behavior):
    def __init__(self, starpath, field, radius):
        super(IgnoEx, self).__init__(starpath, field, radius)
        self.name = "IgnoEx"
        self.origin = None

    def update(self, ball_pos, ball_force):
        if type(ball_pos) != sP.Point:
            ball_pos = sP.Point(None, ball_pos)
        if type(ball_force) != sP.Point:
            ball_force = sP.Point(None, ball_force)

        atTarget = self.starpath.getNearTarget(ball_pos)
        if self.target is None:
            self.target = next(iter(atTarget.journeys))
            self.journey = atTarget.journeys[self.target]
            self.origin = atTarget
            self.nxt_mv = self.journey.smooth.getFirstPoint()

        # 35 -> Target size!
        # reached nxt_mv? Fetch the new nxt_mv and slowDown becauhse
        # in smoothPath/simplepath, every point is a corner
        # if there is no next mv, reverse direction!
        if ball_pos.inRange(self.radius + 10, self.nxt_mv):
            self.nxt_mv = self.nxt_mv.next()

            # there is no next move but we hit the last one(our destination)
            if self.nxt_mv is None:
                if self.journey.collide:
                    del (atTarget.journeys[self.origin])
                    del (self.origin.journeys[atTarget])
                self.target = self.giveNewTarget(atTarget, self.origin)
                self.journey = atTarget.journeys[self.target]
                self.origin = atTarget
                self.nxt_mv = self.journey.smooth.getFirstPoint()
            else:
                return self.slowDown(ball_pos, ball_force)

        return (self.nxt_mv - ball_pos).norm()


# Learning: Es rennt nur 1(eher explorer) oder 2(eher follower) mal in ein unsichtbares obs
# ignorant: Nicht eingehen auf den Mitspieler(nie)
# performance: nimmt leichtesten weg
# follower: Geht auf Mitspieler ein, daher, eher passiv (geht nah mit learning zusammen)
# explorer: Jeden Pfad mal abfahren, sich dabei merken, welcher pfad ohne unsichtbares obs
# perfomance-ignorant
class BestIgno(Behavior):
    def __init__(self, starpath, field, radius):
        super(BestIgno, self).__init__(starpath, field, radius)
        self.name = "BestIgno"
        self.bestJourney = self.starpath.getShortestJourney()
        self.origin = None
        self.counter = 0

    def update(self, ball_pos, ball_force):
        if not isinstance(ball_pos, sP.Point):
            ball_pos = sP.Point(None, ball_pos)
        if not isinstance(ball_force, sP.Point):
            ball_force = sP.Point(None, ball_force)
        atTarget = self.starpath.getNearTarget(ball_pos)

        # init
        if self.target is None:
            self.target = self.starpath.getNearTarget(self.bestJourney.path.getFirstPoint())
            if self.target in atTarget.journeys.keys():
                self.journey = atTarget.journeys[self.target]
            else:
                self.journey = self.bestJourney
            self.origin = atTarget
            self.nxt_mv = self.journey.smooth.getFirstPoint()

        # did we reached our target, where the best journey starts??
        if atTarget == self.target:
            self.target = 0
            self.journey = self.bestJourney
            self.origin = atTarget
            self.nxt_mv = self.journey.smooth.getFirstPoint()

        # bug, kein next() mehr
        if isinstance(self.nxt_mv.next(), sP.Point) and ball_pos.dist(self.nxt_mv) > ball_pos.dist(self.nxt_mv.next()):
            self.nxt_mv = self.nxt_mv.next()

        # 35 -> Target size!
        # reached nxt_mv? Fetch the new nxt_mv and slowDown becauhse
        # in smoothPath/simplepath, every point is a corner
        # if there is no next mv, reverse direction!
        if ball_pos.inRange(self.radius + 10, self.nxt_mv):
            self.nxt_mv = self.nxt_mv.next()

            # there is no next move but we hit the last one(our destination)
            if self.nxt_mv is None:
                if self.journey.collide:
                    self.counter += 1
                # make sure we have learned from our mistakes
                if self.counter == 2:
                    self.counter = 0
                    self.journey = atTarget.journeys[self.giveNewTarget(atTarget, self.origin)]
                    self.origin = atTarget
                    self.nxt_mv = self.journey.smooth.getFirstPoint()
                else:
                    self.journey = atTarget.journeys[self.origin]
                    self.origin = atTarget
                    self.nxt_mv = self.journey.smooth.getFirstPoint()
            else:
                return self.slowDown(ball_pos, ball_force)

        return (self.nxt_mv - ball_pos).norm()

# nimmt immer wieder den am vielversprechendsten Pfad. Dieses kann ein besonders
# kurzer Pfad sein oder ein besonders leicht abzufahrender Pfad, da jedes obstacle
# collision minuspunkte bedeutet und der Ball schwer zu navigieren ist. Er bemerkt
# wenn auf seinem Idealen Pfad unsichtbare Hindernisse liegen und aendert ihn gebenen
# falls. Wenn ihn der gegenspieler gaenzlich von seinem Erfolgspfad abbringt, folgt
# er ihm bis er wieder in die Naehe von seinem Erfolgspfad kommt.
# best perfomance-follower
# class bestFollow(Behavior):


# nimmt immer wieder den am vielversprechendsten Pfad. Dieses kann ein besonders kurzer Pfad sein
# oder ein besonders leicht abzufahrender Pfad, da jedes obstacle collision minuspunkte bedeutet
# und der Ball schwer zu navigieren ist.
# -> nimmt den kürzesten Pfad und bleibt auf diesem
# class bestPerformance(Behavior):

# nimmt keine Ruecksicht auf den Gegenspieler, macht nur sein eigenes
# Ding(evtl einfach default behavior?)
# class ignorant(Behavior):

# ist gaenzlich passiv. sollte jedoch input liefern falls der Gegenspieler nichts mehr
# macht, damit der Spieler nicht denk dass niemand mit spielt.
# class follower(Behavior):