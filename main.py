from globs import *
from game import *
from gui import *
import pygame
import sys

TRENUTNI = BLACK
BOARD = set_board([[EMPTY for _ in range(8)] for _ in range(8)])
add_moves(BOARD, TRENUTNI)
print_board(BOARD, SCORE)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = xy_to_pos(pos[0], pos[1]) if in_table(pos) else (-1, -1)
            if x != -1 and BOARD[x][y] == MOVES:
                BOARD[x][y] = TRENUTNI
                SCORE[TRENUTNI] += 1
                clear_moves(BOARD)
                flip(BOARD, TRENUTNI, x, y)
                TRENUTNI = WHITE if TRENUTNI == BLACK else BLACK
                has_moves = add_moves(BOARD, TRENUTNI)
                print_board(BOARD, SCORE)
                if not has_moves:
                    TRENUTNI = WHITE if TRENUTNI == BLACK else BLACK
                    has_moves = add_moves(BOARD, TRENUTNI)
                    print_board(BOARD, SCORE)
                    if not has_moves:
                        print_game_over()

    pygame.display.update()
