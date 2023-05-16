from pygame import gfxdraw
import pygame
import sys

# podešavanja
WIDTH = 800
HEIGHT = 800
T_BORDER = 64
B_BORDER = 64
L_BORDER = 64
R_BORDER = 64
BLACK = (0, 0, 0)
GREEN = (0, 144, 103)
WHITE = (255, 255, 255)
BACKGROUND = (26, 28, 29)

# često korišćene vrednosti
T_WIDTH = WIDTH - L_BORDER - R_BORDER
T_HEIGHT = HEIGHT - T_BORDER - B_BORDER
RADIUS = int(min(T_WIDTH, T_HEIGHT) / 20)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)
pygame.display.set_caption("Othello")


board = [[0 for _ in range(8)] for _ in range(8)]

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
    gfxdraw.filled_circle(screen, x, y, RADIUS, BLACK)
    gfxdraw.aacircle(screen, x, y, RADIUS, BLACK)
    if(color == WHITE):
        gfxdraw.filled_circle(screen, x, y, RADIUS - 1, WHITE)
        gfxdraw.aacircle(screen, x, y, RADIUS - 1, WHITE)


def set_board():
    pygame.draw.rect(screen, BACKGROUND, pygame.Rect(0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, GREEN, pygame.Rect(L_BORDER, T_BORDER, WIDTH - L_BORDER - R_BORDER, HEIGHT - T_BORDER - B_BORDER))
    for i in range(8):
        pygame.draw.line(screen, BLACK, (L_BORDER + T_WIDTH * i / 8, T_BORDER), (L_BORDER + T_WIDTH * i / 8, HEIGHT - B_BORDER))
        pygame.draw.line(screen, BLACK, (L_BORDER, T_BORDER + T_HEIGHT * i / 8), (WIDTH - R_BORDER, T_BORDER + T_HEIGHT * i / 8))
    for i in range(2):
        gfxdraw.filled_circle(screen, int(L_BORDER + T_WIDTH / 4), int(T_BORDER + T_HEIGHT * (i + 0.5) / 2), 7, BLACK)
        gfxdraw.aacircle(screen, int(L_BORDER + T_WIDTH / 4), int(T_BORDER + T_HEIGHT * (i + 0.5) / 2), 7, BLACK)
        gfxdraw.filled_circle(screen, int(L_BORDER + T_WIDTH * 3 / 4), int(T_BORDER + T_HEIGHT * (i + 0.5) / 2), 7, BLACK)
        gfxdraw.aacircle(screen, int(L_BORDER + T_WIDTH * 3 / 4), int(T_BORDER + T_HEIGHT * (i + 0.5) / 2), 7, BLACK)
        board[3 + i][3 + i] = WHITE
        board[3 + i][4 - i] = BLACK


def print_board():
    for x in range(8):
        for y in range(8):
            if board[x][y]:
                draw_piece(x, y, board[x][y])


set_board()
print_board()
trenutni = WHITE
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] > L_BORDER and pos[0] < WIDTH - R_BORDER and pos[1] > T_BORDER and pos[1] < HEIGHT - B_BORDER:
                x, y = xy_to_pos(pos[0], pos[1])
                trenutni = WHITE if trenutni == BLACK else BLACK
                board[x][y] = trenutni
                print_board()


    pygame.display.update()
