import pygame
from pacman import PacMan
from mappy import Map
# region GLOBAL VARS

# region SIZES
WIDTH, HEIGHT = 850, 550
BLOCK_SIZE = 20
# endregion

# region COLORS
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_PURPLE = (255, 0, 255)
# endregion

# region IMAGE
WALL = pygame.image.load('img/brick.jpg')
WALL = pygame.transform.scale(WALL, (BLOCK_SIZE, BLOCK_SIZE))

BLANK = pygame.image.load('img/black.png')
BLANK = pygame.transform.scale(BLANK, (BLOCK_SIZE, BLOCK_SIZE))

PACMAN = pygame.image.load('img/pac.png')
PACMAN = pygame.transform.scale(PACMAN, (BLOCK_SIZE, BLOCK_SIZE))
PACMAN2 = pygame.image.load('img/pac2.png')
PACMAN2 = pygame.transform.scale(PACMAN2, (BLOCK_SIZE, BLOCK_SIZE))
# endregion

# region OTHERS
FPS = 60
# endregion

# endregion

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ve Map Pygame")

# region UTILS FUNCTION


def draw_map(map: Map):
    for idx_row in range(0, len(map.grid)):
        for idx_col in range(0, len(map.grid[idx_row])):
            val = map.grid[idx_row][idx_col]
            if val == 0:
                posx = idx_col * BLOCK_SIZE
                posy = idx_row * BLOCK_SIZE
                WIN.blit(BLANK, (posx, posy))
            elif val == -1:
                posx = idx_col * BLOCK_SIZE
                posy = idx_row * BLOCK_SIZE
                WIN.blit(WALL, (posx, posy))


def draw_pac(pacman: PacMan, state: int = 1):
    if state == 1:
        WIN.blit(PACMAN, (pacman.cord_x*BLOCK_SIZE, pacman.cord_y*BLOCK_SIZE))
    elif state == 2:
        WIN.blit(PACMAN2, (pacman.cord_x*BLOCK_SIZE, pacman.cord_y*BLOCK_SIZE))


def handle_keyboard(event):
    '''Đổi direction nhưng chưa cập nhật tọa độ pacman'''
    global direction
    if event.key == pygame.K_a:
        direction = "LEFT"
    elif event.key == pygame.K_w:
        direction = "UP"
    elif event.key == pygame.K_d:
        direction = "RIGHT"
    elif event.key == pygame.K_s:
        direction = "DOWN"


def update(state: int):
    '''Thay đổi hiệu ứng hình ảnh cho pacman = cách vẽ lại.
    Bao gồm việc vẽ map vẽ pacman và có thể vẽ ghost'''
    global clock
    WIN.fill(COLOR_WHITE)
    clock.tick(10)
    draw_map(my_map)
    draw_pac(my_pac, state)
    pygame.display.update()


# endregion
my_map = Map()
my_pac = PacMan()
running = True
clock = pygame.time.Clock()
direction = "RIGHT"

while running:
    update(1)
    update(2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        if event.type == pygame.KEYDOWN:
            handle_keyboard(event)

    my_pac.move(direction, my_map)
    clock.tick(FPS)
