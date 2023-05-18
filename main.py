from pygame import gfxdraw
import pygame
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# podešavanja
EMPTY = bcolors.OKGREEN + " ◇"
BLACK = bcolors.OKBLUE + " ◉"
WHITE = bcolors.ENDC + " ◉"
MOVES = bcolors.WARNING + " ◎"
ROBOT_ICON = '󱚝'  # 󱚞 󰚩
USER_ICON = '󰀄'  # 󰀉
PLAYER_W = ROBOT_ICON
PLAYER_B = USER_ICON
SCORE_HEIGHT = 64
SCORE = {WHITE: 2, BLACK: 2}
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
BORDER_POSITIONS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

# često korišćene vrednosti
T_WIDTH = WIDTH - L_BORDER - R_BORDER
T_HEIGHT = HEIGHT - T_BORDER - B_BORDER
RADIUS = min(T_WIDTH, T_HEIGHT) // 20


pygame.init()
font_mdi = pygame.font.Font('mdi.ttf', 64)
font_roboto = pygame.font.Font('roboto.ttf', 64)
font_roboto2 = pygame.font.Font('roboto.ttf', 24)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)
pygame.display.set_caption("Othello")


board = [[EMPTY for _ in range(8)] for _ in range(8)]

def pos_to_xy(x, y):
    return int(L_BORDER + T_WIDTH / 16 + T_WIDTH * x / 8), int(T_BORDER + T_HEIGHT / 16 + T_HEIGHT * y / 8)

def pos_to_x(x):
    return int(L_BORDER + T_WIDTH / 16 + T_WIDTH * x / 8)

def pos_to_y(y):
    return int(T_BORDER + T_HEIGHT / 16 + T_HEIGHT * y / 8)

def xy_to_pos(x, y):
    return min(7, int((x - L_BORDER) / T_WIDTH * 8)), min(7, int((y - T_BORDER) / T_HEIGHT * 8))


def draw_piece(x, y, color):
    x = pos_to_x(x)
    y = pos_to_y(y)

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

def set_score():
    player_b = font_mdi.render(USER_ICON, True, WHITE_C)
    player_w = font_mdi.render(ROBOT_ICON, True, WHITE_C)
    b_box = player_b.get_rect()
    w_box = player_w.get_rect()
    b_box.midleft = (L_BORDER, SCORE_HEIGHT)
    w_box.midright = (WIDTH - R_BORDER, SCORE_HEIGHT)
    screen.blit(player_b, b_box)
    screen.blit(player_w, w_box)

def set_board():
    screen.fill(BACKGROUND_C)
    set_score()
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

def print_game_over():
    text1 = font_roboto2.render('GAME', True, WHITE_C, BACKGROUND_C)
    text2 = font_roboto2.render('OVER', True, WHITE_C, BACKGROUND_C)
    box1 = text1.get_rect()
    box2 = text2.get_rect()
    box1.midbottom = (WIDTH // 2, SCORE_HEIGHT)
    box2.midtop = (WIDTH // 2, SCORE_HEIGHT)
    screen.blit(text1, box1)
    screen.blit(text2, box2)

def print_score():
    score_b = font_roboto.render(str(SCORE[BLACK]), True, WHITE_C, BACKGROUND_C)
    score_w = font_roboto.render(str(SCORE[WHITE]), True, WHITE_C, BACKGROUND_C)
    b_box = score_b.get_rect()
    w_box = score_w.get_rect()
    b_box.midleft = (L_BORDER * 2.5, SCORE_HEIGHT)
    w_box.midright = (WIDTH - R_BORDER * 2.5, SCORE_HEIGHT)
    screen.blit(score_b, b_box)
    screen.blit(score_w, w_box)

def print_board():
    log_board()
    print_score()
    for x in range(8):
        for y in range(8):
            draw_piece(x, y, board[x][y])

def log_board():
    for x in range(8):
        for y in range(8):
            print(board[y][x], end='')
        print()
    print()

def check_pos(x, y, xi, yi):
    return 0 <= x + xi <= 7 and 0 <= y + yi <= 7

def check_line(player, x, y, xi, yi):
    while check_pos(x, y, xi, yi) and (board[x + xi][y + yi] == BLACK or board[x + xi][y + yi] == WHITE):
        if board[x + xi][y + yi] == player:
            return True
        x, y = x + xi, y + yi
    return False

def add_moves(player):
    for x in range(8):
        for y in range(8):
            if board[x][y] == MOVES:
                board[x][y] = EMPTY
    has_moves = False
    opponent = WHITE if player == BLACK else BLACK
    for x in range(8):
        for y in range(8):
            if board[x][y] == opponent:
                for xi, yi in BORDER_POSITIONS:
                    if check_pos(x, y, xi, yi) and board[x + xi][y + yi] == EMPTY and check_line(player, x, y, -xi, -yi):
                        board[x + xi][y + yi] = MOVES
                        has_moves = True
    return has_moves

def flip_line(player, opponent, x, y, xi, yi):
    while board[x][y] == opponent:
        board[x][y] = player
        SCORE[opponent] -= 1
        SCORE[player] += 1
        x, y = x + xi, y + yi

def flip(player, x, y):
    opponent = WHITE if player == BLACK else BLACK
    for xi, yi in BORDER_POSITIONS:
        if check_pos(x, y, xi, yi) and board[x + xi][y + yi] == opponent and check_line(player, x, y, xi, yi):
            flip_line(player, opponent, x + xi, y + yi, xi, yi)

set_board()
trenutni = BLACK
add_moves(trenutni)
print_board()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] > L_BORDER and pos[0] < WIDTH - R_BORDER and pos[1] > T_BORDER and pos[1] < HEIGHT - B_BORDER:
                x, y = xy_to_pos(pos[0], pos[1])
                if board[x][y] == MOVES:
                    SCORE[trenutni] += 1
                    board[x][y] = trenutni
                    flip(trenutni, x, y)
                    trenutni = WHITE if trenutni == BLACK else BLACK
                    has_moves = add_moves(trenutni)
                    print_board()
                    if not has_moves:
                        trenutni = WHITE if trenutni == BLACK else BLACK
                        has_moves = add_moves(trenutni)
                        print_board()
                        if not has_moves:
                            print_game_over()

    pygame.display.update()
