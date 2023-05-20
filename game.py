from pieces import *

BORDER_POSITIONS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

def check_pos(x, y, xi=0, yi=0):
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

def get_moves(board, player):
    moves = []
    opponent = WHITE if player == BLACK else BLACK
    for x in range(8):
        for y in range(8):
            if board[x][y] == opponent:
                for xi, yi in BORDER_POSITIONS:
                    if check_pos(x, y, xi, yi) and board[x + xi][y + yi] == EMPTY and check_line(board, player, x, y, -xi, -yi):
                        moves.append((x + xi, y + yi))
    return moves

def add_moves(board, moves):
    for move in moves:
        board[move[0]][move[1]] = MOVES

def flip_line(board, player, opponent, x, y, xi, yi, score=None):
    while board[x][y] == opponent:
        board[x][y] = player
        x, y = x + xi, y + yi
        if score:
            score[opponent] -= 1
            score[player] += 1

def flip(board, player, x, y, score=None):
    board[x][y] = player
    opponent = WHITE if player == BLACK else BLACK
    for xi, yi in BORDER_POSITIONS:
        if check_pos(x, y, xi, yi) and board[x + xi][y + yi] == opponent and check_line(board, player, x, y, xi, yi):
            flip_line(board, player, opponent, x + xi, y + yi, xi, yi, score)

def switch_trenutni(trenutni):
    return WHITE if trenutni == BLACK else BLACK
