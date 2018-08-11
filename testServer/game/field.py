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
        self.step_size = 10
        self.x = self.y = 0
        self.targets = 0
        self.screenrect = pygame.display.get_surface().get_rect()

    def update(self, events):

        for event in events:
                if event.type == KEYDOWN:
                        if event.key == K_LEFT:
                                self.x += -1 * self.step_size
                        elif event.key == K_RIGHT:
                                self.x += 1 * self.step_size
                        elif event.key == K_UP:
                                self.y += -1 * self.step_size
                        elif event.key == K_DOWN:
                                self.y += 1 * self.step_size
                elif event.type == KEYUP:
                        if event.key in (K_LEFT, K_RIGHT):
                                self.x = 0
                        elif event.key in (K_UP, K_DOWN):
                                self.y = 0
        if self.x and not self.screenrect.contains(self.rect.move(self.x, 0)):
                self.x = 0
        if self.y and not self.screenrect.contains(self.rect.move(0, self.y)):
                self.y = 0
        self.rect.move_ip(self.x, self.y)

    def reset_position(self):
            print("reset position reached in player")
            self.rect.center = self.start_pos

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

    for pos in ((172, 133),(710, 659),(300, 407),(950, 200)):
        c = Target(pos)
        all_sprites.add(c)
        targets.add(c)
    for pos in ((388, 324),(124, 202),(615, 194),(866, 102),(230, 590),(961, 706),(570, 450),(300, 31),(820, 550)):
        b = Obstacle(pos)
        all_sprites.add(b)
        obstacles.add(b)

    while True:
        # maximal 40 fps
        clock.tick(30)
        # events bearbeiten
        events = pygame.event.get()
        for event in events:
        # um möglichst einfach Positionen für die Spielobjekte zu sammeln:
            if event.type == MOUSEBUTTONDOWN:
                print(event.pos)
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
        for target in pygame.sprite.spritecollide(player, targets, True):
                player.targets += 1
        for obstacle in pygame.sprite.spritecollide(player, obstacles, False):
                player.targets -= 1
                player.reset_position()

        # den Bildschirm mit einer Hintergrundfarbe füllen und so
        # gleichzeitig das alte Bild löschen
        screen.fill((100,100,100))

        ## Über die Gruppe alle Sprites updaten und dann blitten
        all_sprites.update(events)
        all_sprites.draw(screen)

        # alles aufs Fenster flippen
        pygame.display.flip()

if __name__ == '__main__': main()
