import calclib
import pygame

# PyGame
pygame.init()
pygame.font.init()
gameDisplay = pygame.display.set_mode((320, 240), pygame.NOFRAME)
pygame.display.set_caption("Dino-Game")
font = pygame.font.SysFont('Roboto', 16)

# Game Clock
clock = pygame.time.Clock()


# noinspection PyBroadException
def main():
    i = ""
    f = ""
    d_x_norm = 10
    d_x = d_x_norm
    keymap = {}

    def use(i):
        expr = i.strip()
        if expr:
            expr = calclib.tokenize(expr)
            expr = calclib.implicit_multiplication(expr)
            expr = calclib.to_rpn(expr)
            res = calclib.eval_rpn(expr)
            print('%g' % res)
            return str(float(res))
        return ""

    while True:
        try:
            gameDisplay.fill([255, 255, 255])

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # EQUALS
                    if event.key == pygame.K_RETURN:
                        f = use(i)
                    # DEL
                    elif event.key == pygame.K_BACKSPACE:
                        i = i[0:len(i)-1]
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
            gameDisplay.blit(textsurface, (310-font.size(f)[0], 55))
            pygame.display.update()
            clock.tick(60)
        except Exception:
            pass


if __name__ == '__main__':
    main()
