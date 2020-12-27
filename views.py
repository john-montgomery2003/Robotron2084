import pygame
import model
from event import *
from characters import Player
from const import *

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
            if currentstate == model.STATE_MENU:
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

        if isinstance(event, Keyboard):
            self.currentDown[event.key] = 1

        if isinstance(event, KeyboardUp):
            self.currentDown[event.key] = 0

        for key in self.currentDown.keys():
            if self.currentDown[key]:
                if key == 119:
                    player.setmovy(-VELOCITY)
                if key == 115:
                    player.setmovy(VELOCITY)
                if key == 97:
                    player.setmovx(-VELOCITY)
                if key == 100:
                    player.setmovx(VELOCITY)


        self.skincount += 1
        if self.skincount > 2:
            self.skincount = 0

        if not self.isinitialized:
            return
        # clear display
        self.screen.fill((10,10,10))
        # draw some words on the screen

        if self.currentDown[97]:
            player.setdir('W')
        if self.currentDown[100]:
            player.setdir('E')
        if self.currentDown[119]:
            player.setdir('N')
        if self.currentDown[115]:
            player.setdir('S')

        somewords = self.smallfont.render(
            'This is a testing screen',
            True,
            (0, 255, 0))
        self.screen.blit(somewords, (225, 0))
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
        self.smallfont = pygame.font.Font(None, 40)
        self.isinitialized = True
        self.player = Player()
