import pygame
from pygame.locals import *
from testServer.game import game
from testServer.game import models

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Ball-Game")
    Game = game.Game(screen, 1337)

    for pos in ((512, 691), (246, 230), (778, 230), (512, 384)):
        Game.addTarget(pos)
    for opt in ([(512, 445), 90], [(459, 353), 210], [(725, 261),330], [(420, 544),20], [(328, 384),100], [(420, 224),80], [(512, 77),180], [(604, 544),280], [(778, 538),300]):
        Game.addObstacle(opt[0], opt[1])

    Game.server.waitForClient()
    Game.server.send_fr(Game.server.trial_def)
    Game.server.send_fr(Game.server.frame)
    mainLoop(Game)


def mainLoop(Game):
    while True:
        receive = Game.server.receive_fr()
        #p1_x = #TODO finding x coordinates from ball position
        #p1_y =
        p1_fx = round(receive["Frame Data"]["X"]) #0.334566544444
        p1_fy = round(receive["Frame Data"]["Y"]) #0.334566544444

        Game.player.applyForces(p1_fx, p1_fy)
        print("applied forces from peer:", p1_fx, p1_fy)
        #Game.server.send_fr(Game.server.frame)
        #print("send frame by server: ", Game.server.getFrame())

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        pos = Game.player.rect.center
        print("pos: ", pos)
        Game.server.p1_x, Game.server.p1_y = Game.server.p2_x, Game.server.p2_y = pos
        print(" p1_x", Game.server.p1_x)
        Game.server.updateFrame()
        Game.server.send_fr(Game.server.frame)
        print("send frame by server: ", Game.server.getFrame())
        Game.update(events)
        Game.draw(p1_fx, p1_fy)
        pygame.display.flip()
        Game.clock.tick(60)

if __name__ == "__main__":
    main()
