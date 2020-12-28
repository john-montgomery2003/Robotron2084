from characters_module.characters import Character

class Player(Character):
    def __init__(self):
        self.sheetname = 'sprites/player.png'
        Character.__init__(self, self.sheetname)