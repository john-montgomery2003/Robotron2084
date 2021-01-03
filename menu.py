import random
import webbrowser

import pygame

from APIinteractions import *
from constants.colors import *
from constants.const import *
from event import *
from states import *

_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, gfcolor=pygame.Color('dodgerblue'), ocolor=(255, 130, 45), opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf

def get_ran_col():
    return random.choice(random_colors)

def randomStart(view):
    for i in range(0, SCREENSIZE[0], 2):
        for j in range(0, SCREENSIZE[1], 2):
            col = get_ran_col()
            rect = pygame.Rect((i, j), (2, 2))
            pygame.draw.rect(view.screen, col, rect)

def allopperational(view):
    view.tickcounter += 1
    if view.tickcounter > 40:
        view.evManager.post(ChangeState(HOMESCREEN))
    elif view.tickcounter > 5:
        view.screen.fill((10, 10, 10))
        todisplay1 = '''Initial tests indicate:'''

        todisplay2 = 'Operational'

        somewords1 = view.font.render(
            todisplay1,
            True,
            WHITE)

        somewords2 = view.font.render(
            todisplay2,
            True,
            WHITE)

        width1, _ = pygame.font.Font.size(view.font, todisplay1)
        position_font1 = (SCREENSIZE[0] - width1) / 2
        view.screen.blit(somewords1, (position_font1, SCREENSIZE[1]/2-50))

        width2, _ = pygame.font.Font.size(view.font, todisplay2)
        position_font2 = (SCREENSIZE[0] - width2) / 2
        view.screen.blit(somewords2, (position_font2, SCREENSIZE[1]/2+50))

    else:
        randomStart(view)
    pygame.display.flip()

    view.clock.tick(TPS)


def home(view, event):
    view.screen.fill(BLACK)
    view.tickcounter += 1
    if isinstance(event, Keyboard):
        if event.key == 32:
            view.evManager.post(ChangeState(PLAYGAME))
        if event.key == 104:
            view.evManager.post(ChangeState(HELP))
        if event.key == 13:
            view.evManager.post(ChangeState(LOGIN))
        if event.key == 111:
            webbrowser.open('https://robo.johnmontgomery.tech', new=2)
    else:
        prog = list(range(40,0,-1))
        if view.tickcounter % 10 == 1:
            view.col = random.choice(title_colors)
            view.edgecol = random.choice(edge)
        for idx, letter in enumerate('ROBOTRON:'):
            image = render(letter, view.largefont, gfcolor=view.col, ocolor=view.edgecol)
            w,h = image.get_width(), image.get_height()
            image = pygame.transform.scale(image, (w, 0 if view.tickcounter<idx else h+int(1.3**prog[view.tickcounter-idx if view.tickcounter- idx<40 else 39])))
            view.screen.blit(image , (88+idx*74,90-image.get_height()/2))

        if 220 >= view.tickcounter > 40:
            view.tickcounter += 2
            image = pygame.image.load('sprites/2084.png')
            w,h = image.get_width(), image.get_height()
            image = pygame.transform.scale(image, (w, 180*h // (view.tickcounter - 40)))
            view.screen.blit(image, (196, (100+ (180*h // (view.tickcounter - 40)))/2 ))
        if 220 < view.tickcounter:
            image = pygame.image.load('sprites/2084.png')
            view.screen.blit(image, (196,140))

            somewords = view.smallfont.render(
                'Created By:',
                True,
                (246, 130, 20))
            width, _ = pygame.font.Font.size(view.smallfont, 'Created By:')
            position_font = (SCREENSIZE[0] - width) / 2
            view.screen.blit(somewords, (position_font + 6, 320))

            somewords = view.smallfont.render(
                'John Montgomery',
                True,
                (246, 130, 20))
            width, _ = pygame.font.Font.size(view.smallfont, 'John Montgomery')
            position_font = (SCREENSIZE[0] - width) / 2
            view.screen.blit(somewords, (position_font + 6, 360))
            if view.tickcounter % 5 == 0:
                if view.color == (0,0,0):
                    view.color = (22, 32, 221)
                else:
                    view.color = (0,0,0)
            somewords = view.font.render(
                'SPACE to PLAY',
                True,
                view.color )
            width, _ = pygame.font.Font.size(view.font, 'SPACE to PLAY')
            position_font = (SCREENSIZE[0] - width) / 2
            view.screen.blit(somewords, (position_font + 6, 400))

            somewords = view.smallfont.render(
                'H for HELP',
                True,
                (22, 32, 221))
            width, _ = pygame.font.Font.size(view.smallfont, 'H for HELP')
            position_font = (SCREENSIZE[0] - width) / 2
            view.screen.blit(somewords, (position_font + 6, 440))

            try:
                with open('.token', 'r')as f:
                    text = f.read().split('>')[2]
                    somewords = view.smallfont.render(
                        'LOGGED IN AS '+text,
                        True,
                        (22, 32, 221))
                    width, _ = pygame.font.Font.size(view.smallfont, 'LOGGED IN AS '+text)
                    position_font = (SCREENSIZE[0] - width) / 2
                    view.screen.blit(somewords, (position_font + 6, 470))
            except FileNotFoundError:
                somewords = view.smallfont.render(
                    'ENTER for LOGIN',
                    True,
                    (22, 32, 221))
                width, _ = pygame.font.Font.size(view.smallfont, 'ENTER for LOGIN')
                position_font = (SCREENSIZE[0] - width) / 2
                view.screen.blit(somewords, (position_font + 6, 470))

            somewords = view.minifont.render(
                '''Leaderboard Avaliable at - robo.johnmontgomery.tech''',
                True,
                random.choice(title_colors))
            width, _ = pygame.font.Font.size(view.minifont, 'Leaderboard Avaliable at - robo.johnmontgomery.tech')
            position_font = (SCREENSIZE[0] - width) / 2
            view.screen.blit(somewords, (position_font + 6, 510))

            somewords = view.minifont.render(
                '(Press o to open link)',
                True,
                (255,255,255))
            width, _ = pygame.font.Font.size(view.minifont, '(Press o to open link)')
            position_font = (SCREENSIZE[0] - width) / 2
            view.screen.blit(somewords, (position_font + 6, 540))

            somewords = view.minifont.render(
                'ORIGIONAL GAME CREATED BY: WILLIAM ELECTRONICS INC.',
                True,
                (246, 130, 20))
            width, _ = pygame.font.Font.size(view.minifont, 'ORIGIONAL GAME CREATED BY: WILLIAM ELECTRONICS INC.')
            position_font = (SCREENSIZE[0] - width) / 2
            view.screen.blit(somewords, (position_font + 6, 570))

    pygame.display.flip()

    view.clock.tick(TPS)

def login(view, event):
    view.screen.fill(BLACK)
    if isinstance(event, Mouse):
        if 340 < event.pos[0] < 460 and 200 < event.pos[1] < 240:
            status = loginuser(view.username, view.password)
            if status:
                view.evManager.post(ChangeState(HOMESCREEN))
            else:
                view.incorrect = 250

        elif 320 < event.pos[0] < 480 and 500 < event.pos[1] < 540:
            success = signupuser(view.username1, view.password1, view.password2, view.initials)
            if success:
                view.evManager.post(ChangeState(HOMESCREEN))
            else:
                view.incorrect = 550

        elif 0 < event.pos[0] < 50 and 0 < event.pos[1] < 50:
            view.evManager.post(ChangeState(HOMESCREEN))


    if view.incorrect:
        somewords = view.smallfont.render(
            'INCORRECT',
            True,
            (200,0,0))
        width, _ = pygame.font.Font.size(view.smallfont, 'INCORRECT')
        position_font = (SCREENSIZE[0] - width) / 2
        view.screen.blit(somewords, (position_font + 6, view.incorrect))

    somewords = view.font.render(
        'LOGIN + SIGN UP',
        True,
        (246, 130, 20))
    width, _ = pygame.font.Font.size(view.font, 'LOGIN + SIGN UP')
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(somewords, (position_font + 6, 20))

    logintext = view.smallfont.render(
        'LOGIN',
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.smallfont, 'LOGIN')
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(logintext, (position_font, 206))

    pygame.draw.rect(view.screen, GREY, pygame.Rect(100, 100, 600, 40), width=3)

    pygame.draw.rect(view.screen, GREY, pygame.Rect(100, 150, 600, 40), width=3)

    pygame.draw.rect(view.screen, GREY, pygame.Rect(340, 200, 120, 40), width=3)

    pygame.draw.lines(view.screen, GREY, False, [(30,10),(10,25), (30, 40)], width=5)

    signup = view.smallfont.render(
        'SIGN UP',
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.smallfont, 'SIGN UP')
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(signup, (position_font, 506))

    pygame.draw.rect(view.screen, GREY, pygame.Rect(100, 300, 600, 40), width=3)

    pygame.draw.rect(view.screen, GREY, pygame.Rect(100, 350, 600, 40), width=3)

    pygame.draw.rect(view.screen, GREY, pygame.Rect(100, 400, 600, 40), width=3)

    pygame.draw.rect(view.screen, GREY, pygame.Rect(100, 450, 600, 40), width=3)

    pygame.draw.rect(view.screen, GREY, pygame.Rect(320, 500, 160, 40), width=3)


    if isinstance(event, Mouse):
        if 100<event.pos[0]<700 and 100<event.pos[1]<140:
            pygame.draw.rect(view.screen, WHITE, pygame.Rect(100,97,600,43), width=5)
            view.highlight = 'username'
        elif 100<event.pos[0]<700 and 150<event.pos[1]<190:
            pygame.draw.rect(view.screen, WHITE, pygame.Rect(100,147,600,43), width=5)
            view.highlight = 'password'
        elif 100<event.pos[0]<700 and 300<event.pos[1]<340:
            pygame.draw.rect(view.screen, WHITE, pygame.Rect(100, 297, 600, 43), width=5)
            view.highlight = 'username1'
        elif 100<event.pos[0]<700 and 350<event.pos[1]<390:
            pygame.draw.rect(view.screen, WHITE, pygame.Rect(100, 347, 600, 43), width=5)
            view.highlight = 'password1'
        elif 100<event.pos[0]<700 and 400<event.pos[1]<440:
            pygame.draw.rect(view.screen, WHITE, pygame.Rect(100, 397, 600, 43), width=5)
            view.highlight = 'password2'
        elif 100<event.pos[0]<700 and 450<event.pos[1]<490:
            pygame.draw.rect(view.screen, WHITE, pygame.Rect(100, 447, 600, 43), width=5)
            view.highlight = 'initials'
        else:
            view.highlight = None
    else:
        if view.highlight:
            if view.highlight == 'username':
                pygame.draw.rect(view.screen, WHITE, pygame.Rect(100, 97, 600, 43), width=5)
            elif view.highlight == 'username1':
                pygame.draw.rect(view.screen, WHITE, pygame.Rect(100, 297, 600, 43), width=5)
            elif view.highlight == 'password1':
                pygame.draw.rect(view.screen, WHITE, pygame.Rect(100, 347, 600, 43), width=5)
            elif view.highlight == 'password2':
                pygame.draw.rect(view.screen, WHITE, pygame.Rect(100, 397, 600, 43), width=5)
            elif view.highlight == 'initials':
                pygame.draw.rect(view.screen, WHITE, pygame.Rect(100, 447, 600, 43), width=5)
            else:
                pygame.draw.rect(view.screen, WHITE, pygame.Rect(100, 147, 600, 43), width=5)

    if isinstance(event, Keyboard):
        if view.highlight:
            if view.highlight == 'username':
                if event.uni != 'backspace' :
                    view.username += event.uni
                else:
                    view.username = view.username[:-1]
                if len(view.username)>40:
                    view.username = view.username[:-1]

            elif view.highlight == 'username1':
                if event.uni != 'backspace' :
                    view.username1 += event.uni
                else:
                    view.username1 = view.username1[:-1]
                if len(view.username1)>40:
                    view.username1 = view.username1[:-1]

            elif view.highlight == 'password1':
                if event.uni != 'backspace' :
                    view.password1 += event.uni
                else:
                    view.password1 = view.password1[:-1]
                if len(view.password1)>40:
                    view.password1 = view.password1[:-1]

            elif view.highlight == 'password2':
                if event.uni != 'backspace' :
                    view.password2 += event.uni
                else:
                    view.password2 = view.password2[:-1]
                if len(view.password2)>40:
                    view.password2 = view.password2[:-1]

            elif view.highlight == 'initials':
                if event.uni != 'backspace' :
                    view.initials += event.uni
                else:
                    view.initials = view.initials[:-1]
                if len(view.initials)>3:
                    view.initials = view.initials[:-1]

            else:
                if event.uni != 'backspace':
                    view.password += event.uni
                else:
                    view.password = view.password[:-1]
                if len(view.password)>40:
                    view.username = view.username[:-1]

    if view.password2 != view.password1:
        pygame.draw.rect(view.screen, RED, pygame.Rect(100, 347, 600, 43), width=5)
        pygame.draw.rect(view.screen, RED, pygame.Rect(100, 397, 600, 43), width=5)

    text = view.tinyfont.render(
        'username',
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.tinyfont, 'username')
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(text, (position_font + 6, 301))

    text = view.minifont.render(
        view.username1,
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.minifont, view.username1)
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(text, (position_font + 6, 311))

    text = view.tinyfont.render(
        'password',
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.tinyfont, 'password')
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(text, (position_font + 6, 351))

    text = view.minifont.render(
        '*'*len(view.password1),
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.minifont, '*'*len(view.password1))
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(text, (position_font + 6, 361))

    text = view.tinyfont.render(
        'confirm password',
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.tinyfont, 'confirm password')
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(text, (position_font + 6, 401))

    text = view.minifont.render(
        '*'*len(view.password2),
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.minifont, '*'*len(view.password2))
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(text, (position_font + 6, 411))

    text = view.tinyfont.render(
        'initials',
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.tinyfont, 'initials')
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(text, (position_font + 6, 451))

    text = view.minifont.render(
        view.initials,
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.minifont, view.initials)
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(text, (position_font + 6, 461))

    text = view.tinyfont.render(
        'username',
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.tinyfont, 'username')
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(text, (position_font + 6, 101))

    usernametext = view.minifont.render(
        view.username,
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.minifont, view.username)
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(usernametext, (position_font + 6, 111))

    text = view.tinyfont.render(
        'password',
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.tinyfont, 'password')
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(text, (position_font + 6, 151))

    passwordtext = view.minifont.render(
        len(view.password) * '*',
        True,
        (255, 255, 255))
    width, _ = pygame.font.Font.size(view.minifont, len(view.password) * '*')
    position_font = (SCREENSIZE[0] - width) / 2
    view.screen.blit(passwordtext, (position_font + 6, 161))


    pygame.display.flip()

    view.clock.tick(TPS)


def endgame(view, event):
    view.screen.fill(BLACK)
    view.tickcounter += 1
    if isinstance(event, Keyboard):
        if event.key == 32:
            view.evManager.post(ChangeState(HOMESCREEN))
        if event.key == 111:
            webbrowser.open('https://robo.johnmontgomery.tech', new=2)
        if event.key == 13:
            view.evManager.post(ChangeState(LOGIN))
    else:
        prog = list(range(40, 0, -1))
        if view.tickcounter % 10 == 1:
            view.col = random.choice(title_colors)
            view.edgecol = random.choice(edge)
        for idx, letter in enumerate('ROBOTRON:'):
            image = render(letter, view.largefont, gfcolor=view.col, ocolor=view.edgecol)
            w, h = image.get_width(), image.get_height()
            image = pygame.transform.scale(image, (w, 0 if view.tickcounter < idx else h + int(
                1.3 ** prog[view.tickcounter - idx if view.tickcounter - idx < 40 else 39])))
            view.screen.blit(image, (88 + idx * 74, 90 - image.get_height() / 2))
        if 220 >= view.tickcounter > 40:
            view.tickcounter += 2
            image = pygame.image.load('sprites/2084.png')
            w, h = image.get_width(), image.get_height()
            image = pygame.transform.scale(image, (w, 180 * h // (view.tickcounter - 40)))
            view.screen.blit(image, (196, (100 + (180 * h // (view.tickcounter - 40))) / 2))
        if 220 < view.tickcounter:
            image = pygame.image.load('sprites/2084.png')
            view.screen.blit(image, (196, 140))

            if view.tickcounter % 5 == 0:
                if view.color == (0, 0, 0):
                    view.color = (22, 32, 221)
                else:
                    view.color = (0, 0, 0)

            somewords = view.font.render(
                'GAME OVER',
                True,
                view.color)
            width, _ = pygame.font.Font.size(view.font, 'GAME OVER')
            position_font = (SCREENSIZE[0] - width) / 2
            view.screen.blit(somewords, (position_font + 6, 330))

            somewords = view.font.render(
                'You scored:',
                True,
                (246, 130, 20))
            width, _ = pygame.font.Font.size(view.font, 'You scored:')
            position_font = (SCREENSIZE[0] - width) / 2
            view.screen.blit(somewords, (position_font + 6, 400))

            somewords = view.font.render(
                str(view.score),
                True,
                (246, 130, 20))
            width, _ = pygame.font.Font.size(view.font, str(view.score))
            position_font = (SCREENSIZE[0] - width) / 2
            view.screen.blit(somewords, (position_font + 6, 450))

            somewords = view.smallfont.render(
                'SPACE for homescreen',
                True,
                (246, 130, 20))
            width, _ = pygame.font.Font.size(view.smallfont, 'SPACE for homescreen')
            position_font = (SCREENSIZE[0] - width) / 2
            view.screen.blit(somewords, (position_font + 6, 500))

            somewords = view.smallfont.render(
                'O to open leaderboard',
                True,
                (246, 130, 20))
            width, _ = pygame.font.Font.size(view.smallfont, 'O to open leaderboard')
            position_font = (SCREENSIZE[0] - width) / 2
            view.screen.blit(somewords, (position_font + 6, 525))

            if checkonline():
                if isloggedin():
                    if addscore(view.score):
                        somewords = view.smallfont.render(
                            'Score added to leaderboard',
                            True,
                            (246, 130, 20))
                        width, _ = pygame.font.Font.size(view.smallfont, 'Score added to leaderboard')
                        position_font = (SCREENSIZE[0] - width) / 2
                        view.screen.blit(somewords, (position_font + 6, 550))
                else:
                    somewords = view.smallfont.render(
                        'Enter to log in',
                        True,
                        (246, 130, 20))
                    width, _ = pygame.font.Font.size(view.smallfont, 'Enter to log in')
                    position_font = (SCREENSIZE[0] - width) / 2
                    view.screen.blit(somewords, (position_font + 6, 550))
            else:
                somewords = view.smallfont.render(
                    'OFFLINE',
                    True,
                    RED)
                width, _ = pygame.font.Font.size(view.smallfont, 'OFFLINE')
                position_font = (SCREENSIZE[0] - width) / 2
                view.screen.blit(somewords, (position_font + 6, 550))
    pygame.display.flip()

    view.clock.tick(TPS)