import pygame
from random import randint

# PyGame
pygame.init()
pygame.font.init()
gameDisplay = pygame.display.set_mode((320, 240), pygame.NOFRAME)
pygame.display.set_caption("Dino-Game")
font = pygame.font.SysFont('Roboto', 16)
# Game Clock
clock = pygame.time.Clock()

# Custom Vars
crashed = False
score = 0

# Colors
c_black = (0, 0, 0)
c_white = (255, 255, 255)

# Images
i_dino_walk0 = pygame.image.load('Dino/dino_walk0.png')
i_dino_walk1 = pygame.image.load('Dino/dino_walk1.png')
i_dino_crawl0 = pygame.image.load('Dino/dino_crawl0.png')
i_dino_crawl1 = pygame.image.load('Dino/dino_crawl1.png')
i_dino_death = pygame.image.load('Dino/dino_death.png')

i_street = pygame.image.load('Dino/street.png')

i_obstacle0_0 = pygame.image.load('Dino/obstacle0_0.png')
i_obstacle0_1 = pygame.image.load('Dino/obstacle0_1.png')
i_obstacle0_2 = pygame.image.load('Dino/obstacle0_2.png')
i_obstacle1_0 = pygame.image.load('Dino/obstacle1_0.png')
i_obstacle1_1 = pygame.image.load('Dino/obstacle1_1.png')

# Background
w, h = i_street.get_size()
x = 0
x1 = w

# Dino
d_x, d_y = 5, 140
d_w, d_h = 44, 49
d_last_state = 0
d_last_update = 2
d_jump_peek = 70
d_normal_y = 140
d_step = 5
d_jumping = False
d_falling = False
d_crawling = False

# Obstacles
obstacle_last_x = w / 2
obstacle_min_dist = int(w / 5)
obstacles = []
obstacle_last_gen = 0


class Obstacle:
    def __init__(self, pos, size, im, type_b=False):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.w = size[0]
        self.h = size[1]
        self.size = size
        self.image = im
        self.type_b = type_b
        self.state = 0
        self.update_count = 0

    def __str__(self):
        return "<Obstacle object x={}, y={}, w={}, h={}>".format(self.x, self.y, self.w, self.h)

    def draw(self):
        gameDisplay.blit(self.image, (self.x, self.y))

    def update(self):
        self.x -= 7
        if self.type_b:
            if self.update_count > 6:
                self.update_count = 0
                if self.state == 0:
                    self.image = i_obstacle1_1
                    self.state = 1
                else:
                    self.image = i_obstacle1_0
                    self.state = 0
            self.update_count += 1


def generate_obstacle(obstacle_type, obstacle_version, pos):
    res = None
    if obstacle_type == 0:
        if obstacle_version == 0:
            res = Obstacle(pos, (51, 35), i_obstacle0_0)
        if obstacle_version == 1:
            res = Obstacle(pos, (34, 35), i_obstacle0_1)
        if obstacle_version == 2:
            res = Obstacle(pos, (17, 35), i_obstacle0_2)
    elif obstacle_type == 1:
        p = randint(0, 1)
        if p == 1:
            pos = (pos[0], pos[1] - 40)
        else:
            pos = (pos[0], pos[1] - 14)
        if obstacle_version == 0:
            res = Obstacle(pos, (46, 46), i_obstacle1_0, True)
        if obstacle_version == 1:
            res = Obstacle(pos, (46, 46), i_obstacle1_1, True)
    return res


def figure(ix, iy, state):
    global d_w, d_h
    img = None
    if not d_crawling:
        if state == 1:
            img = i_dino_walk0
            d_w, d_h = 44, 49
        if state == 2:
            img = i_dino_walk1
            d_w, d_h = 44, 49
    else:
        if state == 1:
            img = i_dino_crawl0
            d_w, d_h = 53, 30
        if state == 2:
            img = i_dino_crawl1
            d_w, d_h = 53, 30
    if state == 3:
        img = i_dino_death

    if img is not None:
        gameDisplay.blit(img, (ix, iy))


if __name__ == "__main__":
    begin_obstacle = generate_obstacle(0, 2, (400, 153))
    obstacles.append(begin_obstacle)
    while not crashed:
        gameDisplay.fill([255, 255, 255])
        d_crawling = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # JUMP
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    keys = pygame.key.get_pressed()
                    if not d_falling and not d_jumping and not d_crawling and not keys[pygame.K_DOWN]:
                        d_jumping = True
                        d_y -= d_step
                # ESCAPE
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # CRAWL
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            if not d_falling and not d_jumping:
                d_crawling = True
                d_y = d_normal_y + 19
        else:
            if not d_falling and not d_jumping:
                d_crawling = False
                d_y = d_normal_y

        # Background
        gameDisplay.blit(i_street, (x, 0))
        gameDisplay.blit(i_street, (x1, 0))

        x -= 7
        x1 -= 7
        if x <= -w:
            x = w
        if x1 <= -w:
            x1 = w

        # OBSTACLES
        if len(obstacles) == 0 or obstacles[len(obstacles) - 1].x < obstacle_min_dist + 10:
            if score > 150:
                o_type = randint(0, 1)
            else:
                o_type = 0
            if o_type == 0:
                o_version = randint(0, 2)
            else:
                o_version = randint(0, 1)
            o_pos = (obstacles[len(obstacles) - 1].x + obstacle_min_dist + randint(0, int(obstacle_min_dist / 2)), 153)
            o = generate_obstacle(o_type, o_version, o_pos)
            obstacles.append(o)
        for i in range(len(obstacles)):
            obstacle = obstacles[i - 1]
            obstacle.update()
            if obstacle.x > -40:
                obstacle.draw()
            else:
                obstacles.remove(obstacle)

        # Dino
        if d_last_update == 6:
            if not d_jumping and not d_falling:
                if d_last_state == 2:
                    d_last_state = 1
                else:
                    d_last_state = 2
                d_last_update = 0
        else:
            d_last_update += 1

        if d_jumping:
            if d_y == d_jump_peek:
                d_falling = True
                d_jumping = False
            else:
                d_y -= d_step

        if d_falling:
            if d_y == d_normal_y:
                d_falling = False
            else:
                d_y += d_step

        for obstacle in obstacles:
            # gameDisplay.fill((255, 0, 0), ((obstacle.x, obstacle.y), (obstacle.w, obstacle.h)))
            if obstacle.x > d_x > obstacle.x - obstacle.w:
                if obstacle.y > d_y > obstacle.y - obstacle.h:
                    exit()

        figure(d_x, d_y, d_last_state)

        # Score
        score += 1
        text = str(int(score / 30))
        textsurface = font.render(text, False, (0, 0, 0))
        gameDisplay.blit(textsurface, (315 - textsurface.get_size()[0], 5))

        # Update
        pygame.display.update()
        clock.tick(60)
