import pygame
import pygame_menu
from time import sleep
from ghost import Ghost
from pacman import PacMan
from mappy import Map
from algo import astar
# region GLOBAL VARS

# region SIZES
WIDTH, HEIGHT = 850, 550
BLOCK_SIZE = 40
pygame.init()
FONT = pygame.font.Font('freesansbold.ttf', 32)
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

DOT = pygame.image.load('img/dot.png')
DOT = pygame.transform.scale(DOT, (BLOCK_SIZE, BLOCK_SIZE))

PACMAN = pygame.image.load('img/pac.png')
PACMAN = pygame.transform.scale(PACMAN, (BLOCK_SIZE, BLOCK_SIZE))
PACMAN2 = pygame.image.load('img/pac2.png')
PACMAN2 = pygame.transform.scale(PACMAN2, (BLOCK_SIZE, BLOCK_SIZE))
GHOST0 = pygame.image.load('img/ghost0.png')
GHOST0 = pygame.transform.scale(GHOST0, (BLOCK_SIZE, BLOCK_SIZE))
GHOST1 = pygame.image.load('img/ghost1.png')
GHOST1 = pygame.transform.scale(GHOST1, (BLOCK_SIZE, BLOCK_SIZE))
# endregion

# region OTHERS
FPS = 60
# endregion

# endregion

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
            elif val == 1:
                posx = idx_col * BLOCK_SIZE
                posy = idx_row * BLOCK_SIZE
                WIN.blit(DOT, (posx, posy))


def draw_pac(pacman: PacMan, state: int = 1):
    if state == 1:
        WIN.blit(PACMAN, (pacman.cord_x*BLOCK_SIZE, pacman.cord_y*BLOCK_SIZE))
    elif state == 2:
        WIN.blit(PACMAN2, (pacman.cord_x*BLOCK_SIZE, pacman.cord_y*BLOCK_SIZE))


def draw_ghost(ghost: Ghost, img_ghost):
    WIN.blit(img_ghost, (ghost.cord_x*BLOCK_SIZE, ghost.cord_y*BLOCK_SIZE))


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
    draw_ghost(my_ghost0, GHOST0)
    draw_ghost(my_ghost1, GHOST1)
    pygame.display.update()


def get_actions_from_path(path: list) -> list:
    '''Nhận vào list các tuple là tọa độ những điểm cần đi qua để đi từ start tới end.
    Trả về list các string là mảng các action tương ứng để đi từ 1 điểm tới điểm kế tiếp'''
    current_position = path[0]
    actions = []
    # Lưu ý:
    # node_position[0] là row trong grid -> là tung của điểm
    # node_position[1] là col trong grid -> là hoành của điểm

    for next_position in path[1:]:
        if next_position[0] == current_position[0] and next_position[1] - current_position[1] == 1:
            actions.append("RIGHT")
        elif next_position[0] == current_position[0] and next_position[1] - current_position[1] == -1:
            actions.append("LEFT")
        elif next_position[1] == current_position[1] and next_position[0] - current_position[0] == 1:
            actions.append("DOWN")
        elif next_position[1] == current_position[1] and next_position[0] - current_position[0] == -1:
            actions.append("UP")
        current_position = next_position
    return actions


def check_lose(pac: PacMan, ghost: Ghost) -> bool:
    '''Thua là khi pac đụng vô ghost'''
    if pac.cord_x == ghost.cord_x and pac.cord_y == ghost.cord_y:
        return True
    return False


def check_win(map: Map) -> bool:
    '''Thắng là khi trên bản đồ không còn ô nào chứa dot(giá trị 1)'''
    if map.remaining_diem() == 0:
        return True
    elif map.remaining_diem() > 0:
        return False


def get_text(text: str, text_color, cord_x, cord_y):
    display_text = FONT.render(text, True, text_color)
    text_surface = display_text.get_rect()
    text_surface.center = (cord_x, cord_y)
    WIN.blit(display_text, text_surface)


# endregion

# region PYGAME_MENU


# endregion
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Pacman Special Edition Nhom 3")

my_map = Map()
my_pac = PacMan(2, 2)
my_ghost0 = Ghost(0, 0)
my_ghost1 = Ghost(5, 6)
clock = pygame.time.Clock()
direction = "RIGHT"
gaming = False
resulting = False
#my_ghost2 = Ghost()


def reset_game():
    global my_map, my_pac, my_ghost0, my_ghost1, resulting
    my_map = Map()
    my_pac = PacMan(2, 2)
    my_ghost0 = Ghost(0, 0)
    my_ghost1 = Ghost(5, 6)
    resulting = False


def game_loop():
    '''Vòng lặp chính của game'''
    global clock, direction, gaming
    ghost_turn = False
    gaming = True
    while gaming:
        # vẽ frame
        update(1)
        update(2)

        # kiểm tra thắng thua
        if check_lose(my_pac, my_ghost0) or check_lose(my_pac, my_ghost1):
            result_loop(True)
            continue
        if check_win(my_map):
            result_loop(False)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gaming = False
                continue
            if event.type == pygame.KEYDOWN:
                handle_keyboard(event)

        my_pac.move(direction, my_map)
        if ghost_turn:
            # ghost 0 di chuyển
            start0 = (my_ghost0.cord_y, my_ghost0.cord_x)
            end = (my_pac.cord_y, my_pac.cord_x)
            path0 = astar(my_map.grid, start0, end)
            if path0 is not None:
                actions = get_actions_from_path(path0)
                my_ghost0.move(actions[0])
            else:
                pass

            # ghost 1 di chuyển
            start1 = (my_ghost1.cord_y, my_ghost1.cord_x)
            end = (my_pac.cord_y, my_pac.cord_x)
            path1 = astar(my_map.grid, start1, end)
            if path1 is not None:
                actions = get_actions_from_path(path1)
                my_ghost1.move(actions[0])
            else:
                pass
            # chỉnh cho frame sau ghost đứng yên vì không làm thay đổi tọa độ
            ghost_turn = False
        else:
            ghost_turn = True
        clock.tick(FPS)


def result_loop(lost: bool):
    '''Vòng lặp kết quả khi thắng hoặc thua'''
    resulting = True
    if lost:
        color_fill = COLOR_RED
        text_display = "Wasted.Killed by Ghosts"
    elif not lost:
        color_fill = COLOR_GREEN
        text_display = f"Get all dots.Well done !!!Total Scores:{my_pac.score}"
    while resulting:
        WIN.fill(color_fill)
        get_text(text_display, COLOR_BLACK, WIDTH//2, HEIGHT//2)
        get_text("Press 1 to continue playing",
                 COLOR_BLACK, WIDTH//2, HEIGHT//2 + 50)
        get_text("Press 2 to go to menu", COLOR_BLACK,
                 WIDTH//2, HEIGHT//2 + 100)
        get_text("Press 3 to exit", COLOR_BLACK, WIDTH//2, HEIGHT//2 + 150)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                resulting = False
                reset_game()


if __name__ == '__main__':
    game_loop()
