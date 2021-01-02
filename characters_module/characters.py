from pygame import sprite, image, transform
from characters_module import sprites
from constants.const import *
from characters_module.sprites import stretech_image

class Character(sprite.Sprite):
    def __init__(self, sheetname, imagecount=12):
        super().__init__()
        self.sheetname = sheetname
        self.spritesheet = image.load(self.sheetname).convert()
        h,w = self.spritesheet.get_height(), self.spritesheet.get_width()/imagecount
        self.images = [transform.scale(sprite_item, (40,40)) for sprite_item in
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

    def movy(self, newMov):
        if (25+BORDER_W < self.position[1] + newMov < SCREENSIZE[1]-BORDER_W*2-30) :
            self.position = (self.position[0], self.position[1] + newMov)


        self.setdir(newMov, 0)

    def movx(self, newMov):
        if (BORDER_W-10 < self.position[0] + newMov < SCREENSIZE[0]-BORDER_W*2 -10):
            self.position =  (self.position[0]+newMov,self.position[1])
        self.setdir(newMov, 1)

    def onstart(self, view):
        view.screen.fill((0, 0, 0))
        img, h = stretech_image(self.images[0], 30-view.tickcounter)
        posx, posy = self.position
        view.screen.blit(img, (posx, posy - h / 2))