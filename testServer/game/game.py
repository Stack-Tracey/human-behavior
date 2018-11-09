import pygame
from testServer.game import models
from testServer.game import gameServer

class Game():
    def __init__(self, screen, port):
        self.screen = screen
        self.server = gameServer.GameServer(port)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.all_sprites = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.player = models.Player((512, 384))
        self.all_sprites.add(self.player)
        self.this_target = False
        self.last_target = False
        self.score = 0
        print("init")

    def addTarget(self, pos):
        c = models.Target(pos)
        self.targets.add(c)
        self.all_sprites.add(c)

    def addObstacle(self, pos, rotation):
        c = models.Obstacle(pos, rotation)
        self.obstacles.add(c)
        self.all_sprites.add(c)

    # update gamelogic
    def update(self, events):
        for target in pygame.sprite.spritecollide(self.player, self.targets, True):
            self.this_target = target
            self.score += 1

        if self.this_target:
            if self.last_target:
                self.all_sprites.add(self.last_target)
                self.targets.add(self.last_target)
            self.last_target = self.this_target
            self.this_target = False

        for obstacle in self.obstacles:
            if(models.circRotatedRectCollide(self.player, obstacle)):
                self.player.slowdown()

        self.all_sprites.update(events)

    def draw(self, afx, afy):
        fps = self.font.render(str(int(self.clock.get_fps())), True, pygame.Color('black'))
        score = self.font.render(str(self.score), True, pygame.Color('black'))
        afx = self.font.render("afx: "+str(afx), True, pygame.Color('yellow'))
        afy = self.font.render("afy: "+str(afy), True, pygame.Color('yellow'))
        fx = self.font.render("avx:"+str(self.player.xv), True, pygame.Color('yellow'))
        fy = self.font.render("avy:" + str(self.player.yv), True, pygame.Color('yellow'))


        self.screen.fill((100, 100, 100))
        self.all_sprites.draw(self.screen)
        self.player.draw(self.screen)
        self.screen.blit(fps, (50, 50))
        self.screen.blit(score, (50,30))
        self.screen.blit(afx, (50, 70))
        self.screen.blit(afy, (50, 90))
        self.screen.blit(fx, (50, 110))
        self.screen.blit(fy, (50, 130))
