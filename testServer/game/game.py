import pygame
import random
# import models, gameServer
from game.models import *
from game import gameServer

"""
1) Der Ball kann beschleunigt werden. Es macht einen Unterschied, ob ich zu einem nahen Punkt steuere
    oder einen Vollausschlag habe weil straight nach oben gelenkt wird.
2) Der Ball besitzt Traegheit, dh er kann keine scharfen Kurven fahren. Je hoeher die Geschwindigkeit,
    desdo hoeher der Radius der entsteht, wenn um eine Kurve gefahren wird.

"""


class Game():
    def __init__(self, screen, port):
        self.screen = screen
        self.server = gameServer.GameServer(port)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        # self.all_sprites = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.player = Player((512, 384))
        # self.all_sprites.add(self.player)
        self.this_target = False
        self.last_target = False
        self.score = 0

    def init(self):
        for pos in ((512, 691), (246, 230), (778, 230), (512, 384)):
            self.addTarget(pos)
        self.genObstacles(9)
        self.server.send_fr(self.server.trial_def)
        self.server.send_fr(self.server.frame)

    def reset(self):
        self.obstacles = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()

    def genObstacles(self, num):
        def noCollisionWithTarget(o):
            for circ in self.targets:
                circ.radius += 3  # just to be sure...
                if self.circRotatedRectCollide(circ, o):
                    circ.radius -= 3
                    return False
                circ.radius -= 3
            return True

        i = 0
        obs = {}
        obs["Obstacles"] = {}
        obs["Obstacles"]["X"] = [512, 459, 725, 420, 328, 420, 512, 604, 778]
        obs["Obstacles"]["Y"] = [445, 353, 261, 544, 384, 224, 77, 544, 538]
        obs["Obstacles"]["Z"] = []
        obs["Obstacles"]["X_size"] = []
        obs["Obstacles"]["Y_size"] = []
        obs["Obstacles"]["Z_size"] = []
        obs["Obstacles"]["Z_angle_deg"] = []  # [90,210,330,20,100,80,180,280,300]
        obs["Obstacles"]["geometric type"] = []
        obs["Obstacles"]["slowdown factor"] = []
        obs["Obstacles"]["visibility"] = []  # [3,3,3,3,3,4,3,4,4]

        while i < num:
            x = obs["Obstacles"]["X"][i]
            y = obs["Obstacles"]["Y"][i]
            # while True:
            #    x = random.randrange(100, 900, 100)
            #    y = random.randrange(100, 700, 100)
            #    if x not in obs["Obstacles"]["X"] or y not in obs["Obstacles"]["Y"]:
            #        break
            y_size = random.randrange(50, 120)
            # y_size = 68.266
            rotation = random.randrange(0, 360, 15)
            # rotation = obs["Obstacles"]["Z_angle_deg"][each]
            visibility = 4 if random.random() <= 0.20 else 3
            # visibility = obs["Obstacles"]["visibility"][each]

            O = Obstacle((x, y), y_size, -rotation, visibility)
            if noCollisionWithTarget(O):
                self.addObstacle(O)

                # obs["Obstacles"]["X"].append(x)
                # obs["Obstacles"]["Y"].append(y)
                obs["Obstacles"]["Z"].append(5)
                obs["Obstacles"]["X_size"].append(25.6)
                obs["Obstacles"]["Y_size"].append(y_size)
                obs["Obstacles"]["Z_size"].append(10)
                obs["Obstacles"]["Z_angle_deg"].append(rotation)
                obs["Obstacles"]["geometric type"].append(1)
                obs["Obstacles"]["slowdown factor"].append(0.05)
                obs["Obstacles"]["visibility"].append(visibility)
                i += 1

        self.server.trial_def["Level Data"]["Obstacles"] = obs["Obstacles"]
        self.server.trial_def["Level Data"]["Nr of Obstacles"] = num

    def addTarget(self, pos):
        c = Target(pos)
        self.targets.add(c)
        # self.all_sprites.add(c)

    def addObstacle(self, c):
        self.obstacles.add(c)
        # self.all_sprites.add(c)

    def circRotatedRectCollide(self, circ, rect):
        backRotatedCircX = math.cos(rect.angle) * (circ.rect.center[0] - rect.rect.centerx) - math.sin(rect.angle) * (
                    circ.rect.center[1] - rect.rect.centery) + rect.rect.centerx
        backRotatedCircY = math.sin(rect.angle) * (circ.rect.center[0] - rect.rect.centerx) + math.cos(rect.angle) * (
                    circ.rect.center[1] - rect.rect.centery) + rect.rect.centery

        closestX = 0
        closestY = 0

        if (backRotatedCircX < rect.oldrect.topleft[0]):
            closestX = rect.oldrect.topleft[0]
        elif (backRotatedCircX > rect.oldrect.topleft[0] + rect.oldrect.width):
            closestX = rect.oldrect.topleft[0] + rect.oldrect.width
        else:
            closestX = backRotatedCircX

        if (backRotatedCircY < rect.oldrect.topleft[1]):
            closestY = rect.oldrect.topleft[1]
        elif (backRotatedCircY > rect.oldrect.topleft[1] + rect.oldrect.height):
            closestY = rect.oldrect.topleft[1] + rect.oldrect.height
        else:
            closestY = backRotatedCircY

        distance = math.sqrt(abs(backRotatedCircX - closestX) ** 2 + abs(backRotatedCircY - closestY) ** 2)

        if (distance < circ.radius):
            return True
        else:
            return False

    # update gamelogic
    def update(self, events):
        for target in pygame.sprite.spritecollide(self.player, self.targets, True):
            self.this_target = target
            self.score += 1

        if self.this_target:
            if self.last_target:
                # self.all_sprites.add(self.last_target)
                self.targets.add(self.last_target)
            self.last_target = self.this_target
            self.this_target = False

        for obstacle in self.obstacles:
            if (self.circRotatedRectCollide(self.player, obstacle)):
                self.player.slowdown()

        # self.all_sprites.update(events)
        self.player.update(events)

    def draw(self, afx, afy):
        fps = self.font.render(str(int(self.clock.get_fps())), True, pygame.Color('black'))
        score = self.font.render(str(self.score), True, pygame.Color('black'))
        afx = self.font.render("afx: " + str(afx), True, pygame.Color('yellow'))
        afy = self.font.render("afy: " + str(afy), True, pygame.Color('yellow'))
        fx = self.font.render("avx:" + str(self.player.xv), True, pygame.Color('yellow'))
        fy = self.font.render("avy:" + str(self.player.yv), True, pygame.Color('yellow'))

        self.screen.fill((100, 100, 100))
        # self.all_sprites.draw(self.screen)
        self.targets.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.player.draw(self.screen)
        self.screen.blit(fps, (50, 50))
        self.screen.blit(score, (50, 30))
        self.screen.blit(afx, (50, 70))
        self.screen.blit(afy, (50, 90))
        self.screen.blit(fx, (50, 110))
        self.screen.blit(fy, (50, 130))