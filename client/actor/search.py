import numpy as np
import client.actor.starpath as sP
import client.actor.behavoir as behavoir


# from actor import starpath as sP
# from actor import behavoir
# from scipy import spatial

class Search:
    def __init__(self, field, targets):
        self.field = field
        self.targets = targets
        self.behavoir = behavoir.DefaultBehavior(sP.StarPath(self.targets, self.field), self.field, 15)

    def go_for_target(self, ball_pos, ball_force, radius):
        ball_pos = sP.Point(None, ball_pos)
        ball_force = sP.Point(None, ball_force)

        return self.behavoir.update(ball_pos, ball_force)

