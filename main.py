# Neophodno je instalirati pygame modul:
# pip install pygame

from game_logic import *
from globals import *
from bot import *
from gui import *
import pygame
import sys

# odigravanje poteza sa proverama da li je isti igrač ponovo na potezu i da li je kraj igre
def do_move(x, y, board, score, trenutni):
    clear_moves(board)
    score[trenutni] += 1
    flip(board, trenutni, x, y, score)
    for i in range(2):
        trenutni = switch_trenutni(trenutni)
        moves = get_moves(board, trenutni)
        if trenutni == USER:
            add_moves(board, moves)
        print_board(board, score, trenutni)
        if moves:
            break
        elif i:
            print_game_over()
            return False, trenutni
    return True, trenutni

def main():
    BOARD = set_board([[EMPTY for _ in range(8)] for _ in range(8)])
    SCORE = {WHITE: 2, BLACK: 2}
    CONTINUE_GAME = True
    TRENUTNI = BLACK

    # za sliučaj da je bot prvi, uvek igra isti prvi potez
    # ko igra prvi se određuje random u globals.py
    if TRENUTNI == BOT:
        SCORE = {USER: 1, BOT: 4}
        BOARD[4][4] = BOT
        BOARD[5][4] = BOT
        TRENUTNI = USER

    add_moves(BOARD, get_moves(BOARD, TRENUTNI))
    print_board(BOARD, SCORE, USER)

    while True:
        # ako je bot na potezu
        if CONTINUE_GAME and TRENUTNI == BOT:
            move = make_move(BOARD)
            CONTINUE_GAME, TRENUTNI = do_move(move[0], move[1], BOARD, SCORE, TRENUTNI)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # ako je korisnik na potezu
            elif CONTINUE_GAME and event.type == pygame.MOUSEBUTTONDOWN and TRENUTNI == USER:
                pos = pygame.mouse.get_pos()
                x, y = xy_to_pos(pos[0], pos[1]) if in_table(pos) else (-1, -1)
                if x != -1 and BOARD[x][y] == MOVES:
                    CONTINUE_GAME, TRENUTNI = do_move(x, y, BOARD, SCORE, TRENUTNI)
        pygame.display.update()

if __name__ == "__main__":
    main()
