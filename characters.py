from pygame import sprite, image, transform
import sprites
import itertools

class Player(sprite.Sprite):
    def __init__(self):
        self.spritesheet = image.load('sprites/player.png').convert()
        l1,l2,l3,r1,r2,r3,f1,f2,f3,u1,u2,u3 = [transform.scale(sprite_item, (40,40))
            for sprite_item in sprites.loadStrip((0,0,13,12),12, self.spritesheet)]
        self.l_images = l1,l2,l3
        self.r_images = r1,r2,r3
        self.f_images = f1,f2,f3
        self.u_images = u1,u2,u3
        self.direction = 'N'
        self.position  = (300,200)
        self.moving = (0,0)

    def getskin(self, count):
        if self.direction[0] == 'N':
            return self.u_images[count]
        elif self.direction[0] == 'S':
            return self.f_images[count]
        elif self.direction[0] == 'W':
            return self.l_images[count]
        elif self.direction[0] == 'E':
            return self.r_images[count]

    def setdir(self, newDir):
        self.direction = newDir

    def setmovy(self, newMov):
        self.position = (self.position[0], self.position[1] + newMov)

    def setmovx(self, newMov):
        self.position =  (self.position[0]+newMov,self.position[1])