from characters_module.characters import Character
from constants.const import TPS

import pygame

class Player(Character):
    def __init__(self):
        self.sheetname = 'sprites/player.png'
        Character.__init__(self, self.sheetname)

