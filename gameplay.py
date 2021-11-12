import pygame
from constants.colors import *
from event import *
from constants.const import *
from objects.bullet import  Bullet
from states import *
import csv
from characters_module.enemy import *
from characters_module.humans import *
from characters_module.player import *
from playsound import playsound
from multiprocessing import Pool
from math import arctan, sqrt
def loadlevel(view, level):
    playsound('audio/change.mp3', block=False)
    with open ('levels/levels.csv') as f:
        print(level)
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


    view.skincount += 1 if view.tickcounter % 2 == 0 else 0
    if view.skincount > 2:
        view.skincount = 0
    playlist = [view.player.position]
    for idx,item in enumerate(view.spriteslist):
        item.update(view.skincount, playlist[idx%len(playlist)])

    if view.tickcounter > 50:
        class Vector:
            def __init__(self,i,j):
                self.i = i
                self.j = j
                self.angle = arctan(i/j)
                self.mag = sqrt(i**2 + j**2)

        def multiply(v1: Vector, v2: Vector):
            return Vector(v1.i*v2.i, v1.j*v2.j)

        def crossProduct(v1: Vector, v2: Vector):
            return v1.i * v2.j - v2.i * v1.j
        def calculateInView(x: grunt, gruntlist):
            inView = []
            gruntlist = gruntlist.remove(x)
            x1,y1 = x.rect[:1]
            viewVect = {
                'N': [Vector(-1,1), Vector(1,1)],
                'E': [Vector(1,1), Vector(-1,1)],
                'S': [Vector(1,-1), Vector(-1,-1)]
                'W': [Vector(-1,-1), Vector(-1,1)]
            }
            p,q = viewVect[x.direction]
            for grunt in gruntlist:
                x2,y2 = grunt.rect[:1]
                a,b,c = p,q, Vector(x2-x1, y2-y1)
                if (crossProduct(b, c)) * (crossProduct(a, c)) >= 0:
                    # TODO add code here for when grunt is between the sight vecors, eg callculate needed values for boids
            return x, inView

        gruntslist = filter(view.spriteslist, key=lambda x:isinstance(x, Grunt))

        f = lambda x:calculateInView(x, gruntslist)
        with Pool() as p:
            positionsInView = p.map(f, gruntslist)

        for item in view.spriteslist:
            if isinstance(item, Bullet):
                for object in view.spriteslist:
                    if -20<item.rect[0]-object.rect[0]<20 and -20<item.rect[1]-object.rect[1]<20  and not isinstance(object, Bullet):
                        if isinstance(object, Grunt) or isinstance(object, Electrode) or isinstance(object, Hulk):
                            object.kill()
                        item.kill()
            if isinstance(item, Electrode) or isinstance(item, Grunt) or isinstance(item, Hulk):
                if -20<item.rect[0]-player.position[0]<20 and -20<item.rect[1]-player.position[1]<20:
                    view.lives -= 1
                    if view.lives > 0:
                        view.evManager.post(ChangeState(view.model.statem.peek() + 101))
                        return
                    else:
                        view.evManager.post(ChangeState(ENDGAME))
            if isinstance(item, Electrode):
                for object in view.spriteslist:
                    if -10 < item.rect[0] - object.rect[0] < 10 and -10 < item.rect[1] - object.rect[1] < 10 and not isinstance(object, Electrode):
                        if isinstance(object, Grunt):
                            object.kill()
            if isinstance(item, Mommies) or isinstance(item, Daddies) or isinstance(item, Mikeys):
                if -20 < item.rect[0] - player.position[0] < 20 and -20 < item.rect[1] - player.position[1] < 20:
                    score = item.die(view)
                    view.score += score

    gruntcount = sum(1 if isinstance(i, Grunt) else 0 for i in view.spriteslist)
    if gruntcount == 0:
        view.evManager.post(ChangeState(view.model.statem.peek() + 101))
        return

    view.spriteslist.draw(view.screen)



    if view.tickcounter > 30:
        player.getskin(view.skincount)
        view.screen.blit(player.getskin(view.skincount), player.position)


    view.clock.tick(TPS)
    # flip the display to show whatever we drew

    pygame.display.flip()