import pygame
import sys
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

    Game.server.waitForClient()

    RUN = True
    while RUN:
        print("Build trial")
        obstacles = models.genObstacles(9)
        for obt in obstacles["obj"]:
            Game.addObstacle(obt)

        Game.server.trial_def["Level Data"]["Obstacles"] = obstacles["Obstacles"]
        Game.server.trial_def["Level Data"]["Nr of Obstacles"] = len(obstacles["obj"])
        Game.server.send_fr(Game.server.trial_def)
        Game.server.send_fr(Game.server.frame)
        RUN = mainLoop(Game)
        Game.obstacles = pygame.sprite.Group()


def mainLoop(Game):
    print("Running mainloop")
    #pdb.Pdb().set_trace()
    countermax = 300
    RUN = True
    while countermax > 0:
        receive = Game.server.receive_fr()
        p1_fx = receive["Frame Data"]["X"] #0.334566544444
        p1_fy = receive["Frame Data"]["Y"] #0.334566544444
        Game.player.applyForces(p1_fx, p1_fy)

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                return False
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    Game.player.keys["K_LEFT"] = 1
                elif event.key == K_RIGHT:
                    Game.player.keys["K_RIGHT"] = 1
                elif event.key == K_UP:
                    Game.player.keys["K_UP"] = 1
                elif event.key == K_DOWN:
                    Game.player.keys["K_DOWN"] = 1
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    Game.player.keys["K_LEFT"] = 0
                elif event.key == K_RIGHT:
                    Game.player.keys["K_RIGHT"] = 0
                elif event.key == K_UP:
                    Game.player.keys["K_UP"] = 0
                elif event.key == K_DOWN:
                    Game.player.keys["K_DOWN"] = 0
        Game.player.applyKeys()

        pos = Game.player.rect.center
        Game.server.p1_x, Game.server.p1_y = Game.server.p2_x, Game.server.p2_y = pos
        Game.server.p1_fx, Game.server.p1_fy = Game.player.xv, Game.player.yv
        Game.server.updateFrame()
        Game.server.send_fr(Game.server.frame)

        Game.update(events)
        Game.draw(p1_fx, p1_fy)
        pygame.display.flip()
        Game.clock.tick(30)
        countermax -= 1
    return True


if __name__ == "__main__":
    if "profile" in sys.argv:
        import hotshot
        import hotshot.stats
        import tempfile
        import os

        print("TEst")
        profile_data_fname = tempfile.mktemp("prf")
        prof = hotshot.Profile(profile_data_fname)
        prof.run('main()')
        del prof
        s = hotshot.stats.load(profile_data_fname)
        s.strip_dirs()
        print("cumulative\n\n")
        s.sort_stats('cumulative').print_stats()
        print("By time.\n\n")
        s.sort_stats('time').print_stats()
        del s
        # clean up the temporary file name.
        try:
            os.remove(profile_data_fname)
        except:
            # may have trouble deleting ;)
            pass
    else:
        main()