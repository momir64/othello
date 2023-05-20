from pieces import *
from game import *
from gui import *
import pygame
import sys

USER = BLACK
TRENUTNI = BLACK
BOT = switch_trenutni(USER)
BOARD = set_board([[EMPTY for _ in range(8)] for _ in range(8)])
SCORE = {WHITE: 2, BLACK: 2}

add_moves(BOARD, get_moves(BOARD, TRENUTNI))
print_board(BOARD, SCORE)
# move = 4
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = xy_to_pos(pos[0], pos[1]) if in_table(pos) else (-1, -1)
            if x != -1 and BOARD[x][y] == MOVES:
                BOARD[x][y] = TRENUTNI
                # move += 1
                # print(move)
                SCORE[TRENUTNI] += 1
                clear_moves(BOARD)
                flip(BOARD, TRENUTNI, x, y, SCORE)
                TRENUTNI = switch_trenutni(TRENUTNI)
                moves = get_moves(BOARD, TRENUTNI)
                add_moves(BOARD, moves)
                print_board(BOARD, SCORE)
                if not moves:
                    TRENUTNI = switch_trenutni(TRENUTNI)
                    moves = get_moves(BOARD, TRENUTNI)
                    add_moves(BOARD, moves)
                    print_board(BOARD, SCORE)
                    if not moves:
                        print_game_over()
        # if SCORE[BLACK] + SCORE[WHITE] != move:
        #     print(f'{SCORE[BLACK]}\t{SCORE[WHITE]}\t{move}')

    pygame.display.update()
