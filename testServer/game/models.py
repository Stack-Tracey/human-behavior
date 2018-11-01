import pygame
import math

from pygame.locals import *

def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print('can`t load image:', name)
        raise SystemExit
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

def circRotatedRectCollide(circ, rect):
    backRotatedCircX = math.cos(rect.angle) * (circ.rect.center[0] - rect.rect.centerx) - math.sin(rect.angle) * (circ.rect.center[1] - rect.rect.centery) + rect.rect.centerx
    backRotatedCircY = math.sin(rect.angle) * (circ.rect.center[0] - rect.rect.centerx) + math.cos(rect.angle) * (circ.rect.center[1] - rect.rect.centery) + rect.rect.centery

    closestX = 0
    closestY = 0

    if (backRotatedCircX  < rect.oldrect.topleft[0]):
        closestX = rect.oldrect.topleft[0]
    elif (backRotatedCircX  > rect.oldrect.topleft[0] + rect.oldrect.width):
        closestX = rect.oldrect.topleft[0] + rect.oldrect.width
    else:
        closestX = backRotatedCircX

    if (backRotatedCircY < rect.oldrect.topleft[1]):
        closestY = rect.oldrect.topleft[1]
    elif (backRotatedCircY > rect.oldrect.topleft[1] + rect.oldrect.height):
        closestY = rect.oldrect.topleft[1] + rect.oldrect.height
    else:
        closestY = backRotatedCircY

    distance = math.sqrt(abs(backRotatedCircX - closestX)**2 + abs(backRotatedCircY - closestY)**2)

    if (distance < circ.radius):
        return True
    else:
        return False


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect  = load_image("game/img/ball.png", -1)
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.start_pos = pos
        self.radius = self.rect.width/2
        self.speed = 4
        self.x = self.y = 0
        self.xv = self.yv = 0
        self.targets = 0
        self.screenrect = pygame.display.get_surface().get_rect()
        self.wait = 0
        self.tar = 0
        self.tar_onhold = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

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
        #place for vector
        self.rect.move_ip(self.xv, self.yv)
        # langsam werden des balles(ausrollen)
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
        self.xv = self.xv * 0.8
        self.yv = self.yv * 0.8

    # hinzufuegen der kraftvektoren des clients
    def applyForces(self, x, y):
        self.xv = self.xv + x
        self.yv = self.yv + y


class Target(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect  = load_image("game/img/target.png", -1)
        x, y = pos
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        #self.rect.center = (1024 - x, 768 - y)
        self.rect.center = (x, y)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, rotation):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,120])
        self.image.fill([255,0,0])
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.angle = math.radians(rotation)
        x, y = pos
        self.rect.center = (1024-x, 768-y)
        self.oldrect = self.rect
        self.image = pygame.transform.rotate(self.image, rotation)
        self.rect = self.image.get_rect()
        #self.rect.center = (1024-x, 768-y)
        self.rect.center = (x, y)
