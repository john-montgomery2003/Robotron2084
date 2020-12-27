
import pygame
from event import *


class KeyboardController:
    def __init__(self, eventManager):
        self.eventManager = eventManager
        eventManager.add_listener(self)

    def notify(self, event):
        if isinstance(event, Tick):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.eventManager.post(EndGame())
                if event.type == pygame.KEYDOWN:
                    if event.key != pygame.K_ESCAPE:
                        self.eventManager.post(Keyboard(event.unicode))
                    else:
                        self.eventManager.post(EndGame())