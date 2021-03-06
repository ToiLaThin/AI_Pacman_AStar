# region CREDIT
# 8 Bit Adventure - By David Renda https://www.fesliyanstudios.com/royalty-free-music/downloads-c/8-bit-music/6
# Boss Time - By David Renda https://www.fesliyanstudios.com/royalty-free-music/downloads-c/8-bit-music/6
# AI learn to play PacMan || Part 1 - Code Bullet https://www.youtube.com/watch?v=qwhXIzNrb9w -> This is the source of the ideas to code this game
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
BLOCK_SIZE = 28
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
WALL_EASY = pygame.image.load('img/brick.jpg')
WALL_HARD = pygame.image.load('img/neon.jpg')
BLANK = pygame.image.load('img/black.png')
DOT = pygame.image.load('img/bigdot.png')
PACMAN = pygame.image.load('img/pac.png')
PACMAN2 = pygame.image.load('img/pac2.png')
GHOST0 = pygame.image.load('img/ghost0.png')
GHOST1 = pygame.image.load('img/ghost1.png')
GHOST2 = pygame.image.load('img/ghost2.gif')
# endregion

# region OTHERS
FPS = 60
DIFFICULTY = 1  # HARD
# endregion

# endregion

# region UTILS FUNCTION


def draw_map(map: Map):
    if DIFFICULTY == 0:
        wall_to_draw = WALL_EASY
    elif DIFFICULTY == 1:
        wall_to_draw = WALL_HARD

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
                WIN.blit(wall_to_draw, (posx, posy))
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


def resize_image():
    global BLOCK_SIZE, WALL_EASY, WALL_HARD, DOT, BLANK
    global GHOST0, GHOST1, GHOST2, PACMAN, PACMAN2
    WALL_EASY = pygame.transform.scale(WALL_EASY, (BLOCK_SIZE, BLOCK_SIZE))
    WALL_HARD = pygame.transform.scale(WALL_HARD, (BLOCK_SIZE, BLOCK_SIZE))
    BLANK = pygame.transform.scale(BLANK, (BLOCK_SIZE, BLOCK_SIZE))
    DOT = pygame.transform.scale(DOT, (BLOCK_SIZE, BLOCK_SIZE))
    PACMAN = pygame.transform.scale(PACMAN, (BLOCK_SIZE, BLOCK_SIZE))
    PACMAN2 = pygame.transform.scale(PACMAN2, (BLOCK_SIZE, BLOCK_SIZE))
    GHOST0 = pygame.transform.scale(GHOST0, (BLOCK_SIZE, BLOCK_SIZE))
    GHOST1 = pygame.transform.scale(GHOST1, (BLOCK_SIZE, BLOCK_SIZE))
    GHOST2 = pygame.transform.scale(GHOST2, (BLOCK_SIZE, BLOCK_SIZE))


def handle_keyboard(event):
    '''?????i direction nh??ng ch??a c???p nh???t t???a ????? pacman'''
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
    '''Thay ?????i hi???u ???ng h??nh ???nh cho pacman = c??ch v??? l???i.
    Bao g???m vi???c v??? map v??? pacman v?? c?? th??? v??? ghost'''
    global clock
    WIN.fill(COLOR_WHITE)
    clock.tick(10)
    draw_map(my_map)
    draw_pac(my_pac, state)
    draw_ghost(my_ghost0, GHOST0)
    draw_ghost(my_ghost1, GHOST1)
    if DIFFICULTY == 1:
        draw_ghost(my_ghost2, GHOST2)
    pygame.display.update()


def get_actions_from_path(path: list) -> list:
    '''Nh???n v??o list c??c tuple l?? t???a ????? nh???ng ??i???m c???n ??i qua ????? ??i t??? start t???i end.
    Tr??? v??? list c??c string l?? m???ng c??c action t????ng ???ng ????? ??i t??? 1 ??i???m t???i ??i???m k??? ti???p'''
    current_position = path[0]
    actions = []
    # L??u ??:
    # node_position[0] l?? row trong grid -> l?? tung c???a ??i???m
    # node_position[1] l?? col trong grid -> l?? ho??nh c???a ??i???m

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
    '''Thua l?? khi pac ?????ng v?? ghost'''
    if pac.cord_x == ghost.cord_x and pac.cord_y == ghost.cord_y:
        return True
    return False


def check_win(map: Map) -> bool:
    '''Th???ng l?? khi tr??n b???n ????? kh??ng c??n ?? n??o ch???a dot(gi?? tr??? 1)'''
    if map.remaining_diem() == 0:
        return True
    elif map.remaining_diem() > 0:
        return False


def get_text(text: str, text_color, cord_x, cord_y):
    display_text = FONT.render(text, True, text_color)
    text_surface = display_text.get_rect()
    text_surface.center = (cord_x, cord_y)
    WIN.blit(display_text, text_surface)


def change_difficulty(a, b):
    # a va b khong de lam gi chi cho du  tham so
    global DIFFICULTY
    if DIFFICULTY == 0:
        DIFFICULTY = 1
    elif DIFFICULTY == 1:
        DIFFICULTY = 0

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

my_map = None
my_pac = PacMan(2, 2)
my_ghost0 = Ghost(0, 0, 4)
my_ghost1 = Ghost(5, 6, 6)
my_ghost2 = Ghost(9, 9, 2)

clock = pygame.time.Clock()
direction = "RIGHT"
gaming = False
resulting = False

# region LOOPS


def reset_game():
    '''S??? ??c d??ng ????? ch???nh ????? kh?? cho game.
    Kh???i t???o l???i game.
    ?????t c??? gaming = True v?? resulting = False.'''
    global my_map, my_pac, my_ghost0, my_ghost1, my_ghost2, resulting, gaming, direction
    global BLOCK_SIZE
    my_map = Map(DIFFICULTY)
    my_pac = PacMan(2, 2)
    if DIFFICULTY == 0:
        my_ghost0 = Ghost(0, 0, 2)
        my_ghost1 = Ghost(5, 6, 1)
        BLOCK_SIZE = 50
    elif DIFFICULTY == 1:
        my_ghost0 = Ghost(0, 0, 4)
        my_ghost1 = Ghost(22, 16, 6)
        my_ghost2 = Ghost(9, 8, 2)
        BLOCK_SIZE = 28

    direction = "RIGHT"
    gaming = True
    resulting = False
    resize_image()  # c???n resize l???i c??c image sau khi ?????i block size t??y theo ????? kh??


def back_menu():
    global gaming, my_map
    reset_game()
    MENU_SOUND.play_open_menu()
    gaming = False


def game_loop():
    '''V??ng l???p ch??nh c???a game'''
    global clock, direction, gaming
    reset_game()  # reset game s??? cho gaming = True v?? resulting = False
    pygame.mixer.music.play(-1)
    while gaming:
        # v??? frame
        update(1)
        update(2)

        # ki???m tra th???ng thua
        if DIFFICULTY == 1:
            if check_lose(my_pac, my_ghost0) or check_lose(my_pac, my_ghost1) or check_lose(my_pac, my_ghost2):
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(PACMAN_DIE_SOUND)
                sleep(1.5)
                result_loop(True)
                continue
        elif DIFFICULTY == 0:
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

        if my_pac.move(direction, my_map) is True:  # True l?? g???p dot
            pygame.mixer.Sound.play(GAME_EAT_SOUND)

        if my_ghost0.turn_curr == my_ghost0.turn_move:
            # ghost 0 di chuy???n khi t???i l?????t c???a n??
            start0 = (my_ghost0.cord_y, my_ghost0.cord_x)
            end = (my_pac.cord_y, my_pac.cord_x)
            path0 = astar(my_map.grid, start0, end)
            if path0 is not None:
                actions = get_actions_from_path(path0)
                my_ghost0.move(actions[0])
                my_ghost0.turn_curr = 0
            else:
                pass
        else:
            my_ghost0.turn_curr += 1

        if my_ghost1.turn_curr == my_ghost1.turn_move:
            # ghost 1 di chuy???n khi t???i l?????t c???a n??, m???i ghost c?? turn_move kh??c nhau n??n
            # t???c ????? di chuy???n s??? ??a d???ng
            start1 = (my_ghost1.cord_y, my_ghost1.cord_x)
            end = (my_pac.cord_y, my_pac.cord_x)
            path1 = astar(my_map.grid, start1, end)
            if path1 is not None:
                actions = get_actions_from_path(path1)
                my_ghost1.move(actions[0])
                my_ghost1.turn_curr = 0
            else:
                pass
            # ch???nh cho frame sau ghost ?????ng y??n v?? kh??ng l??m thay ?????i t???a ?????
        else:
            my_ghost1.turn_curr += 1

        if DIFFICULTY == 1:
            if my_ghost2.turn_curr == my_ghost2.turn_move:
                start2 = (my_ghost2.cord_y, my_ghost2.cord_x)
                end = (my_pac.cord_y, my_pac.cord_x)
                path2 = astar(my_map.grid, start2, end)
                if path2 is not None:
                    actions = get_actions_from_path(path2)
                    my_ghost2.move(actions[0])
                    my_ghost2.turn_curr = 0
                else:
                    pass
            else:
                my_ghost2.turn_curr += 1
        clock.tick(FPS)


def result_loop(lost: bool):
    '''V??ng l???p k???t qu??? khi th???ng ho???c thua'''
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
                    # tho??t resulting loop -> gameloop:replay game
                    reset_game()
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_2:
                    # tho??t resulting loop v?? c??? game loop -> v??? menu
                    back_menu()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    exit()
# endregion


if __name__ == '__main__':
    MENU.add.selector(
        'Mode ', [('Hard', 1), ('Easy', 2)], selection_effect=MENU_SELECTION_EFFECT2, onchange=change_difficulty)
    MENU.add.button('Play', game_loop)
    MENU.add.button('Quit', pygame_menu.events.EXIT)
    MENU.set_sound(MENU_SOUND, recursive=True)
    # code c???a ph???n hi???n th??? menu l??u ?? MENU.mainloop(WIN)
    MENU_SOUND.play_open_menu()
    MENU.mainloop(WIN)
