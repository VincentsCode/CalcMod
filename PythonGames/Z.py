import pygame
import sys

import calclib
import time
from random import randrange as rand

# PyGame
pygame.init()
pygame.font.init()
gameDisplay = pygame.display.set_mode((320, 240), pygame.NOFRAME)
pygame.display.set_caption("Dino-Game")
font = pygame.font.SysFont('Roboto', 16)

# Game Clock
clock = pygame.time.Clock()

# Hotkeys
to_menu = 'm'
t_calc = 'c'


def menu():
    icon_calc = pygame.image.load('Icons/calculator.png')
    icon_dino = pygame.image.load('Icons/dino.png')
    icon_tetris = pygame.image.load('Icons/tetris.png')
    icon_chat = pygame.image.load('Icons/chat.png')

    class menu_item:
        def __init__(self, name, icon, href):
            self.name = name
            self.icon = icon
            self.href = href

        def call(self):
            globals()[self.href]()

        def draw(self, x, y, selected=False):
            gameDisplay.blit(self.icon, (x, y))
            if selected:
                font.set_underline(True)
                textsurface = font.render(self.name, False, (0, 0, 0))
                font.set_underline(False)
            else:
                textsurface = font.render(self.name, False, (0, 0, 0))
            gameDisplay.blit(textsurface, (x, y+55))

    menu_running = True
    menu_items = [menu_item("Rechner", icon_calc, "calc"),
                  menu_item("Dino", icon_dino, "dino"),
                  menu_item("Tetris", icon_tetris, "tetris"),
                  menu_item("Chat", icon_chat, "chat")
                  ]
    item_selected = 0
    while menu_running:
        gameDisplay.fill([255, 255, 255])

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if item_selected < len(menu_items)-1:
                        item_selected += 1
                if event.key == pygame.K_LEFT:
                    if item_selected > 0:
                        item_selected -= 1
                if event.key == pygame.K_RETURN:
                    menu_running = False
                    menu_items[item_selected].call()
                if event.key == pygame.K_c:
                    menu_running = False
                    calc()

        x = 10
        y = 30
        i = 0
        for item in menu_items:
            if i == item_selected:
                item.draw(x, y, True)
            else:
                item.draw(x, y)
            x += 70
            i += 1

        pygame.display.update()
        clock.tick(60)


def calc():
    i = ""
    f = ""
    d_x_norm = 10
    d_x = d_x_norm
    keymap = {}
    calc_running = True

    def use(i):
        expr = i.strip()
        if expr:
            expr = calclib.tokenize(expr)
            expr = calclib.implicit_multiplication(expr)
            expr = calclib.to_rpn(expr)
            res = calclib.eval_rpn(expr)
            print('%g' % res)
            return str(res)
        return ""

    while calc_running:
        try:
            gameDisplay.fill([255, 255, 255])

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # EQUALS
                    if event.key == pygame.K_RETURN:
                        f = use(i)
                    # DEL
                    elif event.key == pygame.K_BACKSPACE:
                        i = i[0:len(i) - 1]
                        f = ""
                    # AC/ON
                    elif event.key == pygame.K_DELETE:
                        i = ""
                        f = ""
                    # MOVE RIGHT
                    elif event.key == pygame.K_RIGHT:
                        if d_x + font.size(i)[0] > 320:
                            d_x -= 5
                    # MOVE LEFT
                    elif event.key == pygame.K_LEFT:
                        if d_x < d_x_norm:
                            d_x += 5
                    elif event.key == pygame.K_m:
                        calc_running = False
                        menu()
                    # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ., e, pi, log(), cos(), hyp(), sin(), ...
                    else:
                        keymap[event.scancode] = event.unicode
                        i += str(event.unicode)
                        if d_x + font.size(i)[0] > 320:
                            d_x -= font.size(str(event.unicode))[0]
                        f = ""
            textsurface = font.render(i, False, (0, 0, 0))
            gameDisplay.blit(textsurface, (d_x, 30))
            textsurface = font.render(f, False, (0, 0, 0))
            gameDisplay.blit(textsurface, (310 - font.size(f)[0], 55))
            pygame.display.update()
            clock.tick(60)
        except Exception:
            pass


def dino():
    print("DINO")
    showWIP()


def tetris():
    print("TETRIS")
    import Tetris
    Tetris.launch(gameDisplay)


def chat():
    print("CHAT")
    showWIP()


def showWIP():
    textsurface = font.render("[WORK IN PROGRESS]", False, (0, 0, 0))
    gameDisplay.blit(textsurface, (160-(font.size("[WORK IN PROGRESS]")[0]/2), 120-font.size("[WORK IN PROGRESS]")[1]))
    pygame.display.update()
    time.sleep(2)
    menu()


if __name__ == "__main__":
    menu()
