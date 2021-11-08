from pygame import sprite, image, transform
from characters_module import sprites
from constants.const import *
from characters_module.sprites import stretech_image

class Character(sprite.Sprite):
    """
    This is a very basic character, from which all the other
    """
    def __init__(self, sheetname, imagecount=12, scale=40):
        super().__init__()
        self.sheetname = sheetname
        self.spritesheet = image.load(self.sheetname).convert()
        h,w = self.spritesheet.get_height(), self.spritesheet.get_width()/imagecount
        self.images = [transform.scale(sprite_item, (scale,scale)) for sprite_item in
                       sprites.loadStrip((0, 0, w, h), imagecount, self.spritesheet)]

        self.direction = 'N'
        self.position  = (300,200)
        self.moving = (0,0)
        self.image = self.images[0]
        self.rect = (300,200)

    def setdir(self, mov, dir):
        if dir:
            if mov > 0:
                self.direction = 'E'
            if mov < 0:
                self.direction = 'W'
        else:
            if mov > 0:
                self.direction = 'S'
            if mov < 0:
                self.direction = 'N'


    def onstart(self, view):
        view.screen.fill((0, 0, 0))
        img, h = stretech_image(self.images[0], 30-view.tickcounter)
        posx, posy = self.position
        view.screen.blit(img, (posx, posy - h / 2))