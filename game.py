from globs import *

BORDER_POSITIONS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

def check_pos(x, y, xi, yi):
    return 0 <= x + xi <= 7 and 0 <= y + yi <= 7

def check_line(board, player, x, y, xi, yi):
    while check_pos(x, y, xi, yi) and (board[x + xi][y + yi] == BLACK or board[x + xi][y + yi] == WHITE):
        if board[x + xi][y + yi] == player:
            return True
        x, y = x + xi, y + yi
    return False

def clear_moves(board):
    for x in range(8):
        for y in range(8):
            if board[x][y] == MOVES:
                board[x][y] = EMPTY

def add_moves(board, player):
    has_moves = False
    opponent = WHITE if player == BLACK else BLACK
    for x in range(8):
        for y in range(8):
            if board[x][y] == opponent:
                for xi, yi in BORDER_POSITIONS:
                    if check_pos(x, y, xi, yi) and board[x + xi][y + yi] == EMPTY and check_line(board, player, x, y, -xi, -yi):
                        board[x + xi][y + yi] = MOVES
                        has_moves = True
    return has_moves

def flip_line(board, player, opponent, x, y, xi, yi):
    while board[x][y] == opponent:
        board[x][y] = player
        SCORE[opponent] -= 1
        SCORE[player] += 1
        x, y = x + xi, y + yi

def flip(board, player, x, y):
    opponent = WHITE if player == BLACK else BLACK
    for xi, yi in BORDER_POSITIONS:
        if check_pos(x, y, xi, yi) and board[x + xi][y + yi] == opponent and check_line(board, player, x, y, xi, yi):
            flip_line(board, player, opponent, x + xi, y + yi, xi, yi)
