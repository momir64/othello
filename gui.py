from pygame import gfxdraw
from globals import *
import pygame

# podešavanja
LOGGING = False
EMPTY_ICON = "\033[92m ◇"
BLACK_ICON = "\033[94m ◉"
WHITE_ICON = "\033[0m ◉"
MOVES_ICON = "\033[93m ◎"
PIECE_ICONS = (EMPTY_ICON, BLACK_ICON, WHITE_ICON, MOVES_ICON)
ROBOT_ICON = '󱚝'          # 󰚩
USER_ICON = '󰀄'           # 󰀉
ROBOT_ICON_OUTLINE = '󱙺'  # 󱚞
USER_ICON_OUTLINE = '󰀓'   # 󰭕
SCORE_HEIGHT = 64
HEIGHT = 800 + SCORE_HEIGHT
WIDTH = 800
T_BORDER = 64 + SCORE_HEIGHT
B_BORDER = 64
L_BORDER = 64
R_BORDER = 64
BLACK_C = (0, 0, 0)
GRAY_C = (32, 32, 32)
GREEN_C = (0, 144, 103)
WHITE_C = (255, 255, 255)
BACKGROUND_C = (32, 32, 32)  # (26, 28, 29)

# često korišćene vrednosti
T_WIDTH = WIDTH - L_BORDER - R_BORDER
T_HEIGHT = HEIGHT - T_BORDER - B_BORDER
RADIUS = min(T_WIDTH, T_HEIGHT) // 20

# pygame podešavanja
pygame.init()
font_mdi = pygame.font.Font('mdi.ttf', 64)
font_roboto = pygame.font.Font('roboto.ttf', 64)
font_roboto2 = pygame.font.Font('roboto.ttf', 24)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)
pygame.display.set_caption("Othello")

# proverava da li su prozor koordinate unutar table
def in_table(pos):
    return pos[0] > L_BORDER and pos[0] < WIDTH - R_BORDER and pos[1] > T_BORDER and pos[1] < HEIGHT - B_BORDER

# pretvara koordinate na tabli u prozor koordinate
def pos_to_xy(x, y):
    return int(L_BORDER + T_WIDTH / 16 + T_WIDTH * x / 8), int(T_BORDER + T_HEIGHT / 16 + T_HEIGHT * y / 8)

# pretvara prozor koordinate u koordinate na tabli
def xy_to_pos(x, y):
    return min(7, int((x - L_BORDER) / T_WIDTH * 8)), min(7, int((y - T_BORDER) / T_HEIGHT * 8))

# iscrtava žeton na prozoru
def draw_piece(x, y, color):
    x, y = pos_to_xy(x, y)

    if color == EMPTY:
        gfxdraw.filled_circle(screen, x, y, RADIUS + 2, GREEN_C)
        gfxdraw.aacircle(screen, x, y, RADIUS + 2, GREEN_C)
    else:
        gfxdraw.filled_circle(screen, x, y, RADIUS, GRAY_C)
        gfxdraw.aacircle(screen, x, y, RADIUS, GRAY_C)

    if color == WHITE:
        gfxdraw.filled_circle(screen, x, y, RADIUS - 1, WHITE_C)
        gfxdraw.aacircle(screen, x, y, RADIUS - 1, WHITE_C)
    elif color == BLACK:
        gfxdraw.filled_circle(screen, x, y, RADIUS - 1, BLACK_C)
        gfxdraw.aacircle(screen, x, y, RADIUS - 1, BLACK_C)
    elif color == MOVES:
        gfxdraw.filled_circle(screen, x, y, RADIUS - 1, GREEN_C)
        gfxdraw.aacircle(screen, x, y, RADIUS - 1, GREEN_C)

# iscrtava ikone igrača
def print_score_icons(trenutni):
    player_b = font_mdi.render(USER_ICON if trenutni == USER else USER_ICON_OUTLINE, True, WHITE_C, BACKGROUND_C)
    player_w = font_mdi.render(ROBOT_ICON if trenutni == BOT else ROBOT_ICON_OUTLINE, True, WHITE_C, BACKGROUND_C)
    b_box = player_b.get_rect()
    w_box = player_w.get_rect()
    b_box.midleft = (L_BORDER, SCORE_HEIGHT)
    w_box.midright = (WIDTH - R_BORDER, SCORE_HEIGHT)
    screen.blit(player_b, b_box)
    screen.blit(player_w, w_box)

# postavlja tablu
def set_board(board):
    screen.fill(BACKGROUND_C)
    pygame.draw.rect(screen, GREEN_C, pygame.Rect(L_BORDER, T_BORDER, WIDTH - L_BORDER - R_BORDER, HEIGHT - T_BORDER - B_BORDER))
    for i in range(9):
        pygame.draw.line(screen, BLACK_C, (L_BORDER + T_WIDTH * i / 8, T_BORDER), (L_BORDER + T_WIDTH * i / 8, HEIGHT - B_BORDER))
        pygame.draw.line(screen, BLACK_C, (L_BORDER, T_BORDER + T_HEIGHT * i / 8), (WIDTH - R_BORDER, T_BORDER + T_HEIGHT * i / 8))
    for i in range(2):
        gfxdraw.filled_circle(screen, int(L_BORDER + T_WIDTH / 4), int(T_BORDER + T_HEIGHT * (i + 0.5) / 2), 7, BLACK_C)
        gfxdraw.aacircle(screen, int(L_BORDER + T_WIDTH / 4), int(T_BORDER + T_HEIGHT * (i + 0.5) / 2), 7, BLACK_C)
        gfxdraw.filled_circle(screen, int(L_BORDER + T_WIDTH * 3 / 4), int(T_BORDER + T_HEIGHT * (i + 0.5) / 2), 7, BLACK_C)
        gfxdraw.aacircle(screen, int(L_BORDER + T_WIDTH * 3 / 4), int(T_BORDER + T_HEIGHT * (i + 0.5) / 2), 7, BLACK_C)
        board[3 + i][3 + i] = WHITE
        board[3 + i][4 - i] = BLACK
    return board

# iscrtava game over tekst
def print_game_over():
    text1 = font_roboto2.render('GAME', True, WHITE_C, BACKGROUND_C)
    text2 = font_roboto2.render('OVER', True, WHITE_C, BACKGROUND_C)
    box1 = text1.get_rect()
    box2 = text2.get_rect()
    box1.midbottom = (WIDTH // 2, SCORE_HEIGHT)
    box2.midtop = (WIDTH // 2, SCORE_HEIGHT)
    screen.blit(text1, box1)
    screen.blit(text2, box2)
    print_score_icons(EMPTY)

# ispisuje score
def print_score(score, trenutni):
    score_l = font_roboto.render(str(score[USER]) + '       ', True, WHITE_C, BACKGROUND_C)
    score_r = font_roboto.render('       ' + str(score[BOT]), True, WHITE_C, BACKGROUND_C)
    l_box = score_l.get_rect()
    r_box = score_r.get_rect()
    l_box.midleft = (L_BORDER * 2.5, SCORE_HEIGHT)
    r_box.midright = (WIDTH - R_BORDER * 2.5, SCORE_HEIGHT)
    screen.blit(score_l, l_box)
    screen.blit(score_r, r_box)
    print_score_icons(trenutni)

# iscrtava tablu
def print_board(board, score, trenutni):
    if LOGGING:
        log_board(board)
    print_score(score, trenutni)
    for x in range(8):
        for y in range(8):
            draw_piece(x, y, board[x][y])

# ispisuje tablu u konzoli
def log_board(board):
    for x in range(8):
        for y in range(8):
            print(PIECE_ICONS[board[y][x]], end='')
        print()
    print()
