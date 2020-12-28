import pygame
import model
from event import *
from characters_module.player import Player
from constants.const import *
from objects.bullet import Bullet
from decorations.border import Border
import random

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """

    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.

        Attributes:
        isinitialized (bool): pygame is ready to draw.
        screen (pygame.Surface): the screen surface.
        clock (pygame.time.Clock): keeps the fps constant.
        smallfont (pygame.Font): a small font.
        """

        self.evManager = evManager
        self.model = model
        evManager.add_listener(self)
        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None
        self.skincount = 0
        self.player = None
        self.currentDown = {
            97: 0,
            100: 0,
            115: 0,
            119: 0
        }
        self.spriteslist = pygame.sprite.Group()
        self.border = Border()
        self.spriteslist.add(self.border)
        self.lastshot = 0

    def notify(self, event_in):
        """
        Receive events posted to the message queue.
        """
        if isinstance(event_in, Start):
            self.initialize()
        elif isinstance(event_in, EndGame):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event_in, Tick) or isinstance(event_in, Keyboard) or isinstance(event_in, KeyboardUp):
            currentstate = self.model.statem.peek()
            if currentstate == model.STATE_TEST:
                self.rendertest(event_in)
            if currentstate == model.STATE_PLAY:
                self.renderplay()
            if currentstate == model.STATE_HELP:
                self.renderhelp()

    def rendermenu(self):
        self.screen.fill((0, 0, 0))

    def rendertest(self, event):
        """
        A testing function - this is used to ensure that all the functions up to here are working
        """
        player = self.player

        if not self.isinitialized:
            return

        if isinstance(event, Keyboard):
            self.currentDown[event.key] = 1

        if isinstance(event, KeyboardUp):
            self.currentDown[event.key] = 0

        shoot = ''
        v = VELOCITY if sum(self.currentDown.values())>1 else DVELOCITY
        for key in self.currentDown.keys():
            if self.currentDown[key]:
                if key == 119:
                    player.movy(-v)
                if key == 115:
                    player.movy(v)
                if key == 97:
                    player.movx(-v)
                if key == 100:
                    player.movx(v)
                if len(shoot) < 3:
                    if key == 105:
                        shoot += 'N'
                    if key == 107:
                        shoot += 'S'
                    if key == 106:
                        shoot += 'W'
                    if key == 108:
                        shoot += 'E'

        if shoot:
            if self.lastshot == 0:
                bullet = Bullet(player.position[0], player.position[1],shoot)
                self.spriteslist.add(bullet)
                self.lastshot += COOLDOWN
            else:
                self.lastshot -= 1


        self.spriteslist.update()
        game_surface = pygame.Surface(SCREENSIZE, pygame.SRCALPHA, 32)
        game_surface = game_surface.convert_alpha()
        self.spriteslist.draw(game_surface)

        self.skincount += random.randint(0,1)
        if self.skincount > 2:
            self.skincount = 0


        # clear display
        self.screen.fill((10,10,10))
        # draw some words on the screen

        somewords = self.smallfont.render(
            'This is a testing screen',
            True,
            (0, 255, 0))
        width, _ = pygame.font.Font.size(self.smallfont, 'This is a testing screen')
        position_font = (SCREENSIZE[0] - width) /2
        self.screen.blit(somewords, (position_font, 0))

        self.screen.blit(game_surface, (0, 0))
        self.screen.blit(player.getskin(self.skincount), player.position)
        self.clock.tick(TPS)
        # flip the display to show whatever we drew

        pygame.display.flip()

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        result = pygame.init()
        pygame.font.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.clock = pygame.time.Clock()
        self.smallfont = pygame.font.Font('font/robotron-2084.ttf', 28)
        self.isinitialized = True
        self.player = Player()
