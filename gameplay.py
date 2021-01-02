import pygame
from constants.colors import *
from event import *
from constants.const import *
from objects.bullet import  Bullet
from states import *
import csv
from characters_module.enemy import *
from characters_module.humans import *

def loadlevel(view, level):

    with open ('levels/levels.csv') as f:
        csvreader = csv.reader(f, delimiter=',' )
        line = 0
        for row in csvreader:
            if line == 0:
                headers = row
            if line == level:
                leveldata = row
            line += 1


    for header,count in zip(headers[1:], leveldata[1:]):
        view.leveldata[header] = count

    for char in view.leveldata.keys():
        for _ in range(int(view.leveldata[char])):
            newobject = eval(f"{char}()")
            view.spriteslist.add(newobject)


    r, g, b = 0,102,102
    view.screen.fill(BLACK)
    for i in range(60):
        if r > 0 and b == 0:
            r -= 17
            g += 17
        if g > 0 and r == 0:
            g -= 17
            b += 17
        if b > 0 and g == 0:
            b -= 17
            r += 17
        pygame.draw.rect(view.screen, (r,g,b), pygame.Rect(200- (i*5 + 10), SCREENSIZE[1]/2 - i*7 + 10, (SCREENSIZE[0]- 2 * (200- (i*5 + 10))), i*14 + 10), width=3)
        view.clock.tick(TPS)
        pygame.display.flip()

    for i in range(60):
        pygame.draw.rect(view.screen, (0,0,0), pygame.Rect(200- (i*5 + 10), SCREENSIZE[1]/2 - i*7 + 10, (SCREENSIZE[0]- 2 * (200- (i*5 + 10))), i*14 + 10), width=3)
        view.clock.tick(TPS+4)
        pygame.display.flip()

    view.evManager.post(ChangeState(100+level))
    return


def level(view, event):
    player = view.player

    if not view.isinitialized:
        return

    view.screen.fill(BLACK)

    if view.tickcounter <= 30:
        view.player.onstart(view)

    view.tickcounter += 1
    if isinstance(event, Keyboard):
        view.currentDown[event.key] = 1

    if isinstance(event, KeyboardUp):
        view.currentDown[event.key] = 0

    shoot = ''

    v = VELOCITY if sum(view.currentDown.values()) > 1 else DVELOCITY
    for key in view.currentDown.keys():

        if view.currentDown[key]:
            if key == 119:
                player.movy(-v)
            if key == 115:
                player.movy(v)
            if key == 97:
                player.movx(-v)
            if key == 100:
                player.movx(v)
            if len(shoot) < 2:
                if key == 105:
                    shoot += 'N'
                if key == 107:
                    shoot += 'S'
                if key == 106:
                    shoot += 'W'
                if key == 108:
                    shoot += 'E'

    if shoot:
        if view.lastshot == 0:
            bullet = Bullet(player.position[0], player.position[1], shoot)
            view.spriteslist.add(bullet)
            view.lastshot += COOLDOWN
        else:
            view.lastshot -= 1

    view.spriteslist.update()
    game_surface = pygame.Surface(SCREENSIZE, pygame.SRCALPHA, 32)
    game_surface = game_surface.convert_alpha()
    view.spriteslist.draw(game_surface)

    view.skincount += 1 if view.tickcounter % 2 == 0 else 0
    if view.skincount > 2:
        view.skincount = 0

    view.screen.blit(game_surface, (0, 0))
    if view.tickcounter > 30:
        view.screen.blit(player.getskin(view.skincount), player.position)


    view.clock.tick(TPS)
    # flip the display to show whatever we drew

    pygame.display.flip()