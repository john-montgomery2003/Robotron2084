from characters_module.characters import Character
import random
from constants.const import *

class Human(Character):
    def __init__(self,sheetname, images=12):
        Character.__init__(self, sheetname, images)
        self.rect = (random.randint(50,SCREENSIZE[0]-50),random.randint(70,SCREENSIZE[1]-50) )

class Mommies(Human):
    def __init__(self):
        self.sheetname = 'sprites/mommies.png'
        Character.__init__(self, self.sheetname)

class Daddies(Human):
    def __init__(self):
        self.sheetname = 'sprites/player.png'
        Character.__init__(self, self.sheetname)

class Mikeys(Human):
    def __init__(self):
        self.sheetname = 'sprites/mikeys.png'
        Character.__init__(self, self.sheetname)