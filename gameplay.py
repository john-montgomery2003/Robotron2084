import pygame
from

def level(view, event):
    level = view.level
    player = view.player

    if not view.isinitialized:
        return

    view.screen.fill(BLACK)

    if view.tickcounter <= 30:
        view.player.onstart(view)

    view.tickcounter += 1
    if isinstance(event, Keyboard):
        view.currentDown[event.key] = 1

    if isinstance(event, KeyboardUp):
        view.currentDown[event.key] = 0

    shoot = ''
    v = VELOCITY if sum(view.currentDown.values()) > 1 else DVELOCITY
    for key in view.currentDown.keys():
        if view.currentDown[key]:
            if key == 119:
                player.movy(-v)
            if key == 115:
                player.movy(v)
            if key == 97:
                player.movx(-v)
            if key == 100:
                player.movx(v)
            if len(shoot) < 2:
                if key == 105:
                    shoot += 'N'
                if key == 107:
                    shoot += 'S'
                if key == 106:
                    shoot += 'W'
                if key == 108:
                    shoot += 'E'

    if shoot:
        if view.lastshot == 0:
            bullet = Bullet(player.position[0], player.position[1], shoot)
            view.spriteslist.add(bullet)
            view.lastshot += COOLDOWN
        else:
            view.lastshot -= 1

    view.spriteslist.update()
    game_surface = pygame.Surface(SCREENSIZE, pygame.SRCALPHA, 32)
    game_surface = game_surface.convert_alpha()
    view.spriteslist.draw(game_surface)

    view.skincount += 1 if view.tickcounter % 2 == 0 else 0
    if view.skincount > 2:
        view.skincount = 0

