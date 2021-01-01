import pygame
from constants import colors as COLS


def getImage(sheet, rectangle):
    """ Grab a single image out of a larger spritesheet
        Pass in the x, y location of the sprite
        and the width and height of the sprite. """

    rect = pygame.Rect(rectangle)

    # Create a new blank image
    image = pygame.Surface(rect.size).convert()

    # Copy the sprite from the large sheet onto the smaller image
    image.blit(sheet, (0, 0), rect)

    # Assuming black works as the transparent color
    image.set_colorkey(COLS.BLACK)

    # Return the image
    return image

# Load a whole bunch of images and return them as a list
def getImages(sheet, rects):
    "Loads multiple images, supply a list of coordinates"
    return [getImage(sheet, rect) for rect in rects]

# Load a whole strip of images
def loadStrip(rect, image_count, sheet):
    "Loads a strip of images and returns them as a list"
    tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
            for x in range(image_count)]
    return getImages(sheet, tups)

def stretech_image(imagenmame, progression, rect=None):
    if isinstance(imagenmame, str):
        sheet = pygame.image.load(imagenmame).convert()
        h, w = sheet.get_height(), sheet.get_width()
        image = pygame.transform.scale(sheet, (w, h + progression ** 2))
        image.set_colorkey(COLS.BLACK)
        return image, h + progression ** 2
    elif rect != None:
        sheet = pygame.image.load(imagenmame).convert()
        image = getImage(sheet, rect)
        h,w = image.get_height(), image.get_width()
        image = pygame.transform.scale(image, (w, h + progression ** 2))
        return image, h + progression ** 2
    else:
        h, w = imagenmame.get_height(), imagenmame.get_width()
        return pygame.transform.scale(imagenmame, (w, h + progression ** 2)), h + progression ** 2