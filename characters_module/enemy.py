
from characters_module.characters import Character
from constants.const import *
import random

class Enemy(Character):
    def __init__(self,sheetname, images=12):
        Character.__init__(self, sheetname, images)
        self.rect = (random.randint(50,SCREENSIZE[0]-50),random.randint(70,SCREENSIZE[1]-50) )

class Grunt(Enemy):
    def __init__(self):
        self.sheetname = 'sprites/grunt.png'
        Enemy.__init__(self, self.sheetname)


class Electrode(Enemy):
    def __init__(self):
        self.sheetname = 'sprites/electrode.png'
        Enemy.__init__(self, self.sheetname,3)
        self.image = random.choice(self.images)


class Hulk(Enemy):
    def __init__(self):
        self.sheetname = 'sprites/hulk.png'
        Enemy.__init__(self, self.sheetname)

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