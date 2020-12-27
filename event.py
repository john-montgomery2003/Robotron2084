
class Event:
    """
    A class which is a super for all other events the system might handle
    """
    def __init__(self):
        self.name = 'Some event'


class EndGame(Event):
    """
    This event is sent at the end of the game
    """
    def __init__(self):
        self.name = 'End Game'


class Start(Event):
    """
    This event is sent at the start of the game
    """
    def __init__(self):
        self.name = 'Start Game'


class Tick(Event):
    """
    A tick
    """
    def __init__(self):
        self.name = 'Tick'

class Keyboard(Event):
    """
    Event for keyboard clicks
    """
    def __init__(self, key):
        self.name = 'Keyboard'
        self.key = key
    def __str__(self):
        return str(self.key)

class Mouse(Event):
    """
    Event for mouse clicks
    """
    def __init__(self, posx, posy, type):
        self.name = 'Mouse'
        self.posx = posx
        self.posy = posy
        self.type = type