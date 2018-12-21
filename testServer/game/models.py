import pygame
import math
from pygame.locals import *

def load_image(name):
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print('can`t load image:', name)
        raise SystemExit
    image = image.convert()
    colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

# statt s = sekunde gilt s = frame
# F in N
# a in m/(s^2)
# V in m/s
# m in kg
# F = m*a
# a = F/m
# Ball hat m
# spieler liefert F
# ball wird um a beschleunigt
# V = V+a*frame
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect  = load_image("game/img/ball.png")
        self.image = pygame.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.start_pos = pos
        self.radius = self.rect.width/2
        self.mass = 5 # 5kg
        self.x, self.y = pos
        self.xv = self.yv = 0
        self.targets = 0
        self.screenrect = pygame.display.get_surface().get_rect()
        self.wait = 0
        self.keys = {}
        self.keys["K_DOWN"] = 0
        self.keys["K_UP"] = 0
        self.keys["K_RIGHT"] = 0
        self.keys["K_LEFT"] = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, events):
        self.x += self.xv
        self.y += self.yv
        tx, ty = self.rect.center
        self.rect.move_ip(round(self.x-tx), round(self.y - ty))

        # langsam werden des balles(ausrollen)
        self.xv = self.xv * 0.95
        self.yv = self.yv * 0.95

        if self.rect.x < 0:
            self.xv = self.xv * (-1)

        if self.rect.y < 0:
            self.yv = self.yv * (-1)

        if self.rect.x > self.screenrect.width - self.rect.width:
            self.xv = self.xv * (-1)

        if self.rect.y > self.screenrect.height - self.rect.height:
            self.yv = self.yv * (-1)

        if (abs(self.yv) < 0.0001):
            self.yv = 0
        if (abs(self.xv) < 0.0001):
            self.xv = 0

    def reset_position(self):
        self.rect.center = self.start_pos
        self.xv = self.yv = 0

    def slowdown(self):
        self.xv = self.xv * 0.8
        self.yv = self.yv * 0.8

    def applyKeys(self):
        if self.keys["K_RIGHT"]:
            self.applyForces(3, 0)
        if self.keys["K_LEFT"]:
            self.applyForces(-3, 0)
        if self.keys["K_UP"]:
            self.applyForces(0, -3)
        if self.keys["K_DOWN"]:
            self.applyForces(0, 3)

    # adding forces of client
    def applyForces(self, Fx, Fy):
        self.xv = self.xv + (Fx / self.mass) * 1 # 1 = Frame, hier die zeiteinheit. Da immer 1 kann weg gelassen werden
        self.yv = self.yv + Fy / self.mass


class Target(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect  = load_image("game/img/target.png")
        x, y = pos
        self.image = pygame.transform.scale(self.image, (70,70))
        self.rect = self.image.get_rect()
        self.radius = 35
        #self.rect.center = (1024 - x, 768 - y)
        self.rect.center = (x, y)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, y_size, rotation, visibility):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([25,y_size])
        self.image.fill([255,0,0] if visibility == 3 else [0,255,0] )
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.angle = math.radians(rotation)
        x, y = pos
        #self.rect.center = (1024-x, 768-y)
        self.rect.center = (x, y)
        self.oldrect = self.rect
        self.image = pygame.transform.rotate(self.image, rotation)
        self.rect = self.image.get_rect()
        #self.rect.center = (1024-x, 768-y)
        self.rect.center = (x, y)