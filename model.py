from event import *

class Game:
    def __init__(self, eventManager):
        self.eventManager = eventManager
        eventManager.add_listener(self)
        self.on = False

    def notify(self, event):
        if isinstance(event, EndGame):
            self.stop()

    def stop(self):
        self.on = False

    def run(self):
        self.on = True
        self.eventManager.post(Start())
        while self.on:
            newTick = Tick()
            self.eventManager.post(newTick)