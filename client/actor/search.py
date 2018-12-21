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

        """
        if self.behavoir == "explorer":
            bewegt sich ueber das ganze Spielfeld und probiert verschiedene Pfade aus.

        if self.behavoir == "best performance":
            nimmt immer wieder den am vielversprechendsten Pfad. Dieses kann ein besonders
            kurzer Pfad sein oder ein besonders leicht abzufahrender Pfad, da jedes obstacle 
            collision minuspunkte bedeutet und der Ball schwer zu navigieren ist. 

        if self.behavoir == "ignorant":
            nimmt keine Ruecksicht auf den gegenspieler, macht nur sein eigenes Ding(evtl einfach
            default behavior?)

        if self.behavoir == "follower":
            ist gaenzlich passiv. sollte jedoch input liefern falls der Gegenspieler nichts mehr 
            macht, damit der Spieler nicht denk dass niemand mit spielt.

     Das hier sind die Endtypen die sich aus den anderen zusammensetzen

        if self.behavoir == "learning-following-explorer": 
            Mischung aus explorer, best performance und follower. Sollte saemtliche Pfade ausprobieren und
            dabei 'lernen' den daraus resultierenden besten Pfad immer wieder zu benutzen. Beim
            exploren versucht er auch heraus zu finden , wo die Hindernisse beim Gegenspieler 
            liegen. 

        if self.behavior == "learning-ignorant-explorer":
            Mischung aus explorer, best performance und ignorant. Sollte saemtliche Pfade ausprobieren und
            dabei 'lernen' den daraus resultierenden besten Pfad immer wieder zu benutzen. Beim
            exploren versucht er nicht heraus zu finden wo die Hindernisse beim Gegenspieler
            liegen, sondern findet nur seinen optimalen Pfad unabhaengig vom Gegenueber.

        if self.behavior == "best perfomance-ignorant":
            nimmt immer wieder den am vielversprechendsten Pfad. Dieses kann ein besonders
            kurzer Pfad sein oder ein besonders leicht abzufahrender Pfad, da jedes obstacle 
            collision minuspunkte bedeutet und der Ball schwer zu navigieren ist. Er ignoriert
            dabei, dass er noch einen Gegenspieler hat.


        if self.behavior == "best perfomance-follower": 
            nimmt immer wieder den am vielversprechendsten Pfad. Dieses kann ein besonders
            kurzer Pfad sein oder ein besonders leicht abzufahrender Pfad, da jedes obstacle 
            collision minuspunkte bedeutet und der Ball schwer zu navigieren ist. Er bemerkt
            wenn auf seinem Idealen Pfad unsichtbare Hindernisse liegen und aendert ihn gebenen
            falls. Wenn ihn der gegenspieler gaenzlich von seinem Erfolgspfad abbringt, folgt
            er ihm bis er wieder in die Naehe von seinem Erfolgspfad kommt.

        """