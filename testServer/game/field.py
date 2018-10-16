# -*- coding: utf-8 -*-
import pygame
from testServer.socket import gameServer
import random
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
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect  = load_image("img/ball.png", -1)
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.start_pos = pos
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
        self.xv = self.xv * 0.9
        self.yv = self.yv * 0.9


class Target(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect  = load_image("img/target.png", -1)
        x, y = pos
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = (1024 - x, 768 - y)
        self.available = False


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, rotation):
        pygame.sprite.Sprite.__init__(self)
        #self.image, self.rect  = load_image("img/obstacle.png", -1)
        self.image = pygame.Surface([30,120])
        self.image.fill([255,0,0])
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        x, y = pos
        self.rect.center = (1024-x, 768-y)
        #self.image = pygame.transform.scale(self.image, (30,120))
        self.image = pygame.transform.rotate(self.image, rotation)
        self.rect.center = (1024-x, 768-y)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Ball-Game")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    targets = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    player = Player((512, 384))
    all_sprites.add(player)
    last_target = False
    this_target = False

    for pos in ((512, 691), (246, 230), (778, 230), (512, 384)):
        c = Target(pos)
        c.available = True
        all_sprites.add(c)
        targets.add(c)

    for opt in ([(512, 445), 90], [(459, 353), 210], [(725, 261),330], [(420, 544),20], [(328, 384),100], [(420, 224),80], [(512, 77),180], [(604, 544),280], [(778, 538),300]):
        b = Obstacle(opt[0], opt[1])
        all_sprites.add(b)
        obstacles.add(b)

    game_server = gameServer.GameServer(1337)
    game_server.waitForClient()

    #gameloop als Klasse definieren
    fr_nr = 0
    while True:
        if fr_nr < 1:
            trial_def = {"MsgType": "Trial Definition",
                         "Level Data": {"Trial Type": 1, "Trial Duration [ms]": 60000, "Nr of Targets": 4,
                                        "Nr of Obstacles": 9, "Ball": {"X": 512, "Y": 384, "Z": 15, "Radius": 15},
                                        "Targets": {"X": [512, 246, 778, 512], "Y": [691, 230, 230, 384],
                                                    "Z": [5, 5, 5, 5], "Z_size": [10, 10, 10, 10],
                                                    "Radius": [35, 35, 35, 35]},
                                        "Obstacles": {"X": [512, 459, 725, 420, 328, 420, 512, 604, 778],
                                                      "Y": [445, 353, 261, 544, 384, 224, 77, 544, 538],
                                                      "Z": [5, 5, 5, 5, 5, 5, 5, 5, 5],
                                                      "X_size": [25.600000000000001421, 25.600000000000001421,
                                                                 25.600000000000001421, 25.600000000000001421,
                                                                 25.600000000000001421, 25.600000000000001421,
                                                                 25.600000000000001421, 25.600000000000001421,
                                                                 25.600000000000001421],
                                                      "Y_size": [68.266666666666694141, 68.266666666666694141,
                                                                 68.266666666666694141, 102.40000000000000568,
                                                                 102.40000000000000568, 102.40000000000000568,
                                                                 153.59999999999999432, 102.40000000000000568,
                                                                 153.59999999999999432],
                                                      "Z_size": [10, 10, 10, 10, 10, 10, 10, 10, 10],
                                                      "Z_angle_deg": [90, 210, 330, 20, 100, 80, 180, 280, 300],
                                                      "geometric type": [1, 1, 1, 1, 1, 1, 1, 1, 1],
                                                      "slowdown factor": [0.050000000000000002776,
                                                                          0.050000000000000002776,
                                                                          0.050000000000000002776,
                                                                          0.050000000000000002776,
                                                                          0.050000000000000002776,
                                                                          0.050000000000000002776,
                                                                          0.050000000000000002776,
                                                                          0.050000000000000002776,
                                                                          0.050000000000000002776],
                                                      "visibility": [3, 3, 3, 3, 3, 4, 3, 4, 4]}, "AI Type": 0,
                                        "AI 1 Length of Memory": 18,
                                        "Questionair Text": "I didnt define a cool Questionair Text .. :(",
                                        "Blink_Wavelength_Screen": 40, "Blink_Wavelength_OWG": 255,
                                        "Screen_Flicker_Target_Radius": 20, "Max Force": 0.00050000002374872565269,
                                        "ShowBar": "false", "Nr_of_Frames_to_Skip_at_Start_of_Trial": 120,
                                        "Show_Fixation_Cross": "true", "Visibility per Frame - Ball- Player 1": [],
                                        "Visibility per Frame - Targets - Player 1": [],
                                        "Visibility per Frame - Obstacles - Player 1": [],
                                        "Visibility per Frame - Obstacles 2 - Player 1": [],
                                        "Visibility per Frame - Ball- Player 2": [],
                                        "Visibility per Frame - Targets - Player 2": [],
                                        "Visibility per Frame - Obstacles - Player 2": [],
                                        "Visibility per Frame - Obstacles 2 - Player 2": [], "Replay File": "",
                                        "Replay X Position Ball Player 1": [], "Replay Y Position Ball Player 1": [],
                                        "Replay Z Position Ball Player 1": [], "Replay X Position Ball Player 2": [],
                                        "Replay Y Position Ball Player 2": [], "Replay Z Position Ball Player 2": [],
                                        "Replay Trigger States": [], "Replay X Axis Rotation Ball Player 1": [],
                                        "Replay Y Axis Rotation Ball Player 1": [],
                                        "Replay Z Axis Rotation Ball Player 1": [],
                                        "Replay Angle Rotation Ball Player 1": [],
                                        "Replay X Axis Rotation Ball Player 2": [],
                                        "Replay Y Axis Rotation Ball Player 2": [],
                                        "Replay Z Axis Rotation Ball Player 2": [],
                                        "Replay Angle Rotation Ball Player 2": [],
                                        "Nr_of_Frames_to_Show_Fixation_Cross": 120}, "Current Trial Nr.": 1}

            frame = {"MsgType": "Frame",
                     "Frame Data": {"dt [ms]": 0, "Frame Nr.": fr_nr, "Trial Elapsed [ms]": 0, "Trigger State": 544,
                                       "Trial Start [ms]": 0, "Last Frame Start [ms]": 0, "ODE processed until [ms]": 0,
                                    "Player 1": {"X": 512, "Y": 384, "F_x": 0, "F_y": 0, "norm_avg_x": 0,
                                                 "norm avg y": 0, "norm_avg_reshaped_x": 0, "norm avg_reshaped y": 0},
                                    "Player 2": {"X": 512, "Y": 384, "F_x": 0, "F_y": 0, "norm_avg_x": 0,
                                                 "norm avg y": 0, "norm_avg_reshaped_x": 0, "norm avg_reshaped y": 0}}}

            game_server.send_fr(trial_def)
            game_server.send_fr(frame)
        fr_nr += 1

        resp = game_server.receive_fr()
        p1_x = resp["Frame Data"]["X"]
        p1_y = resp["Frame Data"]["Y"]
        p1_fx = 0.334566544444
        p1_fy = 0.334566544444

        #player who generates frame data
        p2_x = 512
        p2_y = 384
        p2_fx = 0
        p2_fy = 0
        frame = {"MsgType": "Frame",
                 "Frame Data": {"dt [ms]": 0, "Frame Nr.": fr_nr, "Trial Elapsed [ms]": 0, "Trigger State": 544,
                                "Trial Start [ms]": 0, "Last Frame Start [ms]": 0, "ODE processed until [ms]": 0,
                                "Player 1": {"X": p1_x, "Y": p1_y, "F_x": p1_fx, "F_y": p1_fy, "norm_avg_x": 0,
                                             "norm avg y": 0, "norm_avg_reshaped_x": 0, "norm avg_reshaped y": 0},
                                "Player 2": {"X": p2_x, "Y": p2_y, "F_x": p2_fx, "F_y": p1_fy, "norm_avg_x": 0,
                                             "norm avg y": 0, "norm_avg_reshaped_x": 0, "norm avg_reshaped y": 0}}}
        game_server.send_fr(frame)

        #--------------------------------------
        clock.tick(30)
        events = pygame.event.get()
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                #print(event.pos)
                i = 0 #just so something happends
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                print(player.rect.center)
                #print(event.type)
                if event.key == K_ESCAPE:
                    return

        collected = False
        for target in pygame.sprite.spritecollide(player, targets, True):
            this_target = target
        if this_target:
            if last_target:
                all_sprites.add(last_target)
                targets.add(last_target)
            last_target = this_target
            this_target = False

        for obstacle in pygame.sprite.spritecollide(player, obstacles, False):
            player.slowdown()

        screen.fill((100,100,100))

        all_sprites.update(events)
        all_sprites.draw(screen)
        player.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()

