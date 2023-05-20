from pieces import *
from game import *
from bot import *
from gui import *
import pygame
import sys

BOARD = set_board([[EMPTY for _ in range(8)] for _ in range(8)])
SCORE = {WHITE: 2, BLACK: 2}

if TRENUTNI == BOT:
    SCORE = {USER: 1, BOT: 4}
    BOARD[5][4] = BOT
    TRENUTNI = USER

def do_move(x, y, board, score):
    global TRENUTNI
    clear_moves(board)
    score[TRENUTNI] += 1
    flip(board, TRENUTNI, x, y, score)
    for i in range(2):
        TRENUTNI = switch_trenutni(TRENUTNI)
        moves = get_moves(board, TRENUTNI)
        if TRENUTNI == USER:
            add_moves(board, moves)
        print_board(board, score)
        if moves:
            break
        elif i:
            print_game_over()

add_moves(BOARD, get_moves(BOARD, TRENUTNI))
print_board(BOARD, SCORE)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif TRENUTNI == BOT and not GAME_OVER:
            move = make_move(BOARD)
            do_move(move[0], move[1], BOARD, SCORE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = xy_to_pos(pos[0], pos[1]) if in_table(pos) else (-1, -1)
            if x != -1 and BOARD[x][y] == MOVES:
                do_move(x, y, BOARD, SCORE)
    pygame.display.update()







# add_moves(BOARD, get_moves(BOARD, TRENUTNI))
# print_board(BOARD, SCORE)
# move = 4 ################
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             pos = pygame.mouse.get_pos()
#             x, y = xy_to_pos(pos[0], pos[1]) if in_table(pos) else (-1, -1)
#             if x != -1 and BOARD[x][y] == MOVES:
#                 BOARD[x][y] = TRENUTNI
#                 SCORE[TRENUTNI] += 1
#                 clear_moves(BOARD)
#                 move += 1   ################
#                 print(move) ################
#                 flip(BOARD, TRENUTNI, x, y, SCORE)
#                 for i in range(2):
#                     TRENUTNI = switch_trenutni(TRENUTNI)
#                     moves = get_moves(BOARD, TRENUTNI)
#                     add_moves(BOARD, moves)
#                     print_board(BOARD, SCORE)
#                     if moves:
#                         break
#                     elif i:
#                         print_game_over()
#         if SCORE[BLACK] + SCORE[WHITE] != move:               ################
#             print(f'{SCORE[BLACK]}\t{SCORE[WHITE]}\t{move}')  ################
#     pygame.display.update()
