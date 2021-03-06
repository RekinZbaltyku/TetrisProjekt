
import pygame
import random

colors = [
    (255, 255, 255),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class Figure:
    x = 0
    y = 0

    figures = [
        [[0]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    sqr_size = 20
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(3, 0)
  
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.stop()

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x
    
    def stop(self):
        self.field[self.figure.y][self.figure.x] = self.figure.color
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def intersects(self):
        intersection = False
        if self.figure.y > self.height - 1 or \
                self.figure.x > self.width - 1 or \
                self.figure.x < 0 or \
                self.field[self.figure.y][self.figure.x] > 0:
            intersection = True
        return intersection
  

# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // 5) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)

    screen.fill(BLACK)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.sqr_size * j, game.y + game.sqr_size * i, game.sqr_size, game.sqr_size], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.sqr_size * j + 1, game.y + game.sqr_size * i + 1, game.sqr_size - 2, game.sqr_size - 1])

    if game.figure is not None:
        pygame.draw.rect(screen, colors[game.figure.color],
                            [game.x + game.sqr_size * (game.figure.x) + 1,
                            game.y + game.sqr_size * (game.figure.y) + 1,
                            game.sqr_size - 2, game.sqr_size - 2])

    font = pygame.font.SysFont('Arial', 65, True, False)
    text_game_over = font.render("Game Over", True, (255, 125, 0))

    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
     

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

