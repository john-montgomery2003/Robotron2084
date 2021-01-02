from characters_module.characters import Character
from constants.const import TPS

import pygame

class Player(Character):
    def __init__(self):
        self.sheetname = 'sprites/player.png'
        Character.__init__(self, self.sheetname)
        self.l_images = self.images[:3]
        self.r_images = self.images[3:6]
        self.f_images = self.images[6:9]
        self.u_images = self.images[9:12]

    def getskin(self, count):
        if self.direction[0] == 'N':
            return self.u_images[count]
        elif self.direction[0] == 'S':
            return self.f_images[count]
        elif self.direction[0] == 'W':
            return self.l_images[count]
        elif self.direction[0] == 'E':
            return self.r_images[count]