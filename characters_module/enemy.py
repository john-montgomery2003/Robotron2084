from pygame import sprite, image

class Enemy(sprite.Sprite):
    def __index__(self):
        sprite.Sprite.__init__(self)
        self.image = None

    