
from characters_module.characters import Character
from constants.const import *
import random
import math
import pygame
class Enemy(Character):
    """
    This enemy is again, only used to extend from. It acts as a basic super class which can easily be used to generate
    the other classes for the enemies. Because the enemies need to update in different ways, its not possible to
    """
    def __init__(self,sheetname, images=12):
        Character.__init__(self, sheetname, images)
        self.rect = (random.randint(50,SCREENSIZE[0]-50),random.randint(70,SCREENSIZE[1]-50) )



class Grunt(Enemy):
    def __init__(self):
        self.sheetname = 'sprites/grunt.png'
        Enemy.__init__(self, self.sheetname)

    def update(self, count, playerpos):
        self.image = self.images[count]
        position = self.rect
        x = playerpos[0] - position[0] +random.randint(-100,100)
        y = playerpos[1] - position[1] + random.randint(-100, 100)
        legnth = sqrt(x**2 + y**2)
        adj = legnth / 3
        newy = y / adj
        newx = x / adj
        self.rect = (self.rect[0]+newx, self.rect[1]+newy)

class Electrode(Enemy):
    def __init__(self):
        self.sheetname = 'sprites/electrode.png'
        Enemy.__init__(self, self.sheetname,3)
        self.image = random.choice(self.images)
        self.image = pygame.transform.scale(self.image, (20,20))
    def update(self, count, _):
        return


class Hulk(Enemy):
    def __init__(self):
        self.sheetname = 'sprites/hulk.png'
        Enemy.__init__(self, self.sheetname)
        self.living = 0

    def getskin(self, count):
        if self.velocity[0] < 0:
            return self.images[:3][count]
        elif self.velocity[0] > 0:
            return self.images[3:6][count]
        elif self.velocity[1] < 0:
            return self.images[6:9][count]
        elif self.velocity[1] > 0:
            return self.images[9:12][count]
        else:
            return self.images[0]

    def update(self, count, _):
        if not self.living % 25:
            self.velocity = (random.choice((-3, 3, 0)), random.choice((-3, 3, 0)))
        flag = False
        while not flag:
            if (35 + BORDER_W < self.rect[1] + self.velocity[1] < SCREENSIZE[1] - BORDER_W * 2 - 35):
                self.rect = (self.rect[0], self.rect[1] + self.velocity[1])
                flag = True
            else:
                self.velocity = (random.choice((-4, 4, 0)), random.choice((-4, 4, 0)))
            if (BORDER_W - 20 < self.rect[0] + self.velocity[0] < SCREENSIZE[0] - BORDER_W * 2 - 20):
                self.rect = (self.rect[0] + self.velocity[0], self.rect[1])
            else:
                self.velocity = (random.choice((-4, 4, 0)), random.choice((-4, 4, 0)))

        self.living += 1

        self.image = self.getskin(count)

    def kill(self):
        self.velocity = (random.choice((-2, 2, 0)), random.choice((-2, 2, 0)))
        flag = False
        while not flag:
            if (35 + BORDER_W < self.rect[1] + self.velocity[1] < SCREENSIZE[1] - BORDER_W * 2 - 35):
                self.rect = (self.rect[0], self.rect[1] + self.velocity[1])
                flag = True
            else:
                self.velocity = (random.choice((-3, 3, 0)), random.choice((-3, 3, 0)))
            if (BORDER_W - 20 < self.rect[0] + self.velocity[0] < SCREENSIZE[0] - BORDER_W * 2 - 20):
                self.rect = (self.rect[0] + self.velocity[0], self.rect[1])
            else:
                self.velocity = (random.choice((-3, 3, 0)), random.choice((-3, 3, 0)))

class Brain(Enemy):
    def __init__(self):
        self.sheetname = 'sprites/brain.png'
        Enemy.__init__(self, self.sheetname)


class Spheroids(Enemy):
    def __init__(self):
        self.sheetname = 'sprites/spheroids.png'
        Enemy.__init__(self, self.sheetname, 8)


class Quarks(Enemy):
    def __init__(self):
        self.sheetname = 'sprites/quark.png'
        Enemy.__init__(self, self.sheetname, 8)


class Enforcer(Enemy):
    def __init__(self):
        self.sheetname = 'sprites/enforcer.png'
        Enemy.__init__(self, self.sheetname, 6)
        self.image = self.images[1]

class Tank(Enemy):
    def __init__(self):
        self.sheetname = 'sprites/tank.png'
        Enemy.__init__(self, self.sheetname, 4)