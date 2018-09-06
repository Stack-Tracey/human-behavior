# -*- coding: utf-8 -*-
import pygame
import random
from pygame.locals import *


def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
        if name == "img/obstacle.png" and random.randint(0, 10) % 2==0:
            image = pygame.transform.rotate(image, 90)

    except pygame.error:
        print('Cannot load image:', name)
        raise SystemExit
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect  = load_image("img/ball.png", -1)
        self.rect.center = pos
        self.start_pos = pos
        self.speed = 4
        self.x = self.y = 0
        self.xv = self.yv = 0
        self.targets = 0
        self.screenrect = pygame.display.get_surface().get_rect()
        self.wait = 0
        self.tar = 0

    def update(self, events):
        for event in events:
                if event.type == KEYDOWN:
                        if event.key == K_LEFT:
                                self.xv += -1 * self.speed
                        elif event.key == K_RIGHT:
                                self.xv += 1 * self.speed
                        elif event.key == K_UP:
                                self.yv += -1 * self.speed
                        elif event.key == K_DOWN:
                                self.yv += 1 * self.speed
                elif event.type == KEYUP:
                        if event.key in (K_LEFT, K_RIGHT):
                                self.x = self.x
                        elif event.key in (K_UP, K_DOWN):
                                self.y = self.y
        if self.x and not self.screenrect.contains(self.rect.move(self.x, 0)):
                self.x = 0
        if self.y and not self.screenrect.contains(self.rect.move(0, self.y)):
                self.y = 0
        self.rect.move_ip(self.xv, self.yv)
        self.xv = self.xv * 0.96
        self.yv = self.yv * 0.96

        if self.rect.x < 0:
            self.xv = self.xv * (-1)

        if self.rect.y < 0:
            self.yv = self.yv * (-1)

        if self.rect.x > self.screenrect.width - self.rect.width:
            self.xv = self.xv * (-1)

        if self.rect.y > self.screenrect.height - self.rect.height:
            self.yv = self.yv * (-1)

    def reset_position(self):
        self.rect.center = self.start_pos
        self.xv = self.yv = 0

    def slowdown(self):
        self.xv = self.xv * 0.9
        self.yv = self.yv * 0.9


class Target(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect  = load_image("img/target.png", -1)
        self.rect.center=pos


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect  = load_image("img/obstacle.png", -1)
        self.rect.center = pos


def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Ball-Game")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    targets = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    player = Player((500, 550))
    all_sprites.add(player)

    for pos in ((172, 133), (710, 659), (300, 407), (950, 200)):
        c = Target(pos)
        all_sprites.add(c)
        targets.add(c)
    for pos in ((388, 324), (124, 202), (615, 194), (866, 102), (230, 590), (961, 706), (570, 450), (300, 31), (820, 550)):
        b = Obstacle(pos)
        all_sprites.add(b)
        obstacles.add(b)

    while True:
        clock.tick(30)
        events = pygame.event.get()
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                print(event.pos)
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

        for target in pygame.sprite.spritecollide(player, targets, True):
            player.wait = 120
            player.targets += 1
            print("player targets", player.targets)
        player.wait -= 1
        if player.wait == 0:
            all_sprites.add(target)
            targets.add(target)

        for obstacle in pygame.sprite.spritecollide(player, obstacles, False):
            player.slowdown()

        screen.fill((100,100,100))

        all_sprites.update(events)
        all_sprites.draw(screen)

        pygame.display.flip()

if __name__ == '__main__': main()