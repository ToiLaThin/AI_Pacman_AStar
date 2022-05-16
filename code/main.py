# region CREDIT
# 8 Bit Adventure - By David Renda https://www.fesliyanstudios.com/royalty-free-music/downloads-c/8-bit-music/6
# Boss Time - By David Renda https://www.fesliyanstudios.com/royalty-free-music/downloads-c/8-bit-music/6
# endregion

import pygame
import pygame_menu
from pygame_menu import sound
from time import sleep
import os
from ghost import Ghost
from pacman import PacMan
from mappy import Map
from algo import astar
pygame.init()

# region GLOBAL VARS

# region SIZES
WIDTH, HEIGHT = 850, 550
BLOCK_SIZE = 40
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

# region SOUND
MENU_SOUND = sound.Sound()
MENU_SOUND.set_sound(sound.SOUND_TYPE_CLICK_MOUSE,
                     os.path.join('sound', 'click.mp3'), volume=1)
MENU_SOUND.set_sound(sound.SOUND_TYPE_WIDGET_SELECTION,
                     os.path.join('sound', 'nav.mp3'), volume=1)
MENU_SOUND.set_sound(sound.SOUND_TYPE_OPEN_MENU,
                     os.path.join('sound', 'intro.mp3'), volume=0.8, loops=1,)


GAME_EAT_SOUND = pygame.mixer.Sound(os.path.join('sound', 'eat.mp3'))
GAME_WIN_SOUND = pygame.mixer.Sound(os.path.join('sound', 'win.mp3'))
GAME_LOST_SOUND = pygame.mixer.Sound(os.path.join('sound', 'lost.mp3'))
PACMAN_DIE_SOUND = pygame.mixer.Sound(os.path.join('sound', 'die.mp3'))
# GAME PLAYING MUSIC
pygame.mixer.music.load(os.path.join('sound', 'playing.mp3'))

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

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Game Pacman Special Edition Nhom 3")
# region PYGAME_MENU
MENU_FONT = pygame_menu.font.FONT_8BIT
MENU_BACKGROUND_IMG = pygame_menu.baseimage.BaseImage(
    image_path=os.path.join('img', 'title.jpg'), drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
MENU_SELECTION_EFFECT1 = pygame_menu.widgets.LeftArrowSelection(
    arrow_size=(10, 15), arrow_right_margin=5, arrow_vertical_offset=0, blink_ms=0)
MENU_SELECTION_EFFECT2 = pygame_menu.widgets.HighlightSelection(
    border_width=4, margin_x=2, margin_y=1)
MENU_THEME = pygame_menu.Theme(background_color=MENU_BACKGROUND_IMG, title_background_color=(2, 2, 2), title_font=MENU_FONT, title_font_size=22, title_font_color=COLOR_WHITE,
                               widget_font=MENU_FONT, widget_font_size=18, widget_font_color=COLOR_YELLOW, widget_selection_effect=MENU_SELECTION_EFFECT1, selection_color=COLOR_RED)
MENU = pygame_menu.Menu("PACMAN SPECIAL EDITION NHOM 3", WIDTH - 200, HEIGHT - 200,
                        theme=MENU_THEME)
# endregion

my_map = Map()
my_pac = PacMan(2, 2)
my_ghost0 = Ghost(0, 0)
my_ghost1 = Ghost(5, 6)
clock = pygame.time.Clock()
direction = "RIGHT"
gaming = False
resulting = False
#my_ghost2 = Ghost()

# region LOOPS


def reset_game():
    '''Sẽ đc dùng để chỉnh độ khó cho game.
    Khởi tạo lại game.
    Đặt cờ gaming = True và resulting = False.'''
    global my_map, my_pac, my_ghost0, my_ghost1, resulting, gaming, direction
    my_map = Map()
    my_pac = PacMan(2, 2)
    my_ghost0 = Ghost(0, 0)
    my_ghost1 = Ghost(5, 6)
    direction = "RIGHT"
    gaming = True
    resulting = False


def back_menu():
    global gaming
    reset_game()
    MENU_SOUND.play_open_menu()
    gaming = False


def game_loop():
    '''Vòng lặp chính của game'''
    global clock, direction, gaming
    reset_game()  # reset game sẽ cho gaming = True và resulting = False
    pygame.mixer.music.play(-1)
    ghost_turn = False
    while gaming:
        # vẽ frame
        update(1)
        update(2)

        # kiểm tra thắng thua
        if check_lose(my_pac, my_ghost0) or check_lose(my_pac, my_ghost1):
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(PACMAN_DIE_SOUND)
            sleep(1.5)
            result_loop(True)
            continue
        if check_win(my_map):
            pygame.mixer.music.stop()
            result_loop(False)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gaming = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                handle_keyboard(event)

        if my_pac.move(direction, my_map) is True:  # True là gặp dot
            pygame.mixer.Sound.play(GAME_EAT_SOUND)

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
    global gaming, resulting
    resulting = True
    if lost:
        color_fill = COLOR_RED
        text_display = "Wasted.Killed by Ghosts"
        pygame.mixer.Sound.play(GAME_LOST_SOUND)
    elif not lost:
        color_fill = COLOR_GREEN
        text_display = f"Get all dots.Well done !!!Total Scores:{my_pac.score}"
        pygame.mixer.Sound.play(GAME_WIN_SOUND)
    while resulting:

        WIN.fill(color_fill)
        get_text(text_display, COLOR_BLACK, WIDTH//2, HEIGHT//2)
        get_text("Press 1 to replay",
                 COLOR_BLACK, WIDTH//2, HEIGHT//2 + 50)
        get_text("Press 2 to go to menu", COLOR_BLACK,
                 WIDTH//2, HEIGHT//2 + 100)
        get_text("Press 3 to exit", COLOR_BLACK, WIDTH//2, HEIGHT//2 + 150)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # thoát resulting loop -> gameloop:replay game
                    reset_game()
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_2:
                    # thoát resulting loop và cả game loop -> về menu
                    back_menu()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    exit()
# endregion


if __name__ == '__main__':
    #
    MENU.add.selector(
        'Mode ', [('Hard', 1), ('Easy', 2)], selection_effect=MENU_SELECTION_EFFECT2)
    MENU.add.button('Play', game_loop)
    MENU.add.button('Quit', pygame_menu.events.EXIT)
    MENU.set_sound(MENU_SOUND, recursive=True)
    # code của phần hiển thị menu lưu ý MENU.mainloop(WIN)
    MENU_SOUND.play_open_menu()
    MENU.mainloop(WIN)
