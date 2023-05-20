from main import USER
from main import BOT
from pieces import *
from game import *

CORNERS = ((0, 0), (0, 7), (7, 0), (7, 7))
SUB_CORNERS = (((0, 1), (1, 0), (1, 1)), ((0, 6), (1, 6), (1, 7)), ((6, 0), (6, 1), (7, 1)), ((6, 6), (6, 7), (7, 6)))
BOARD_VALUES = ((20, -3, 11, +8, +8, 11, -3, 20),
                (-3, -7, -4, +1, +1, -4, -7, -3),
                (11, -4, +2, +2, +2, +2, -4, 11),
                (+8, +1, +2, -3, -3, +2, +1, +8),
                (+8, +1, +2, -3, -3, +2, +1, +8),
                (11, -4, +2, +2, +2, +2, -4, 11),
                (-3, -7, -4, +1, +1, -4, -7, -3),
                (20, -3, 11, +8, +8, 11, -3, 20))

def heuristic_function(board):
    usr_tiles = 0
    bot_tiles = 0
    usr_front_tiles = 0
    bot_front_tiles = 0
    p, c, l, m, f, d = 0, 0, 0, 0, 0, 0

    for x in range(8):
        for y in range(8):
            if board[x][y] == USER:
                d += BOARD_VALUES[x][y]
                usr_tiles += 1
            elif board[x][y] == BOT:
                d -= BOARD_VALUES[x][y]
                bot_tiles += 1
            if board[x][y] != EMPTY:
                for xi, yi in BORDER_POSITIONS:
                    if check_pos(x + xi, y + yi) and board[x + xi][y + yi] == EMPTY:
                        if board[x][y] == USER:
                            usr_front_tiles += 1
                        else:
                            bot_front_tiles += 1
                        break

    p = (100.0 * (usr_tiles if usr_tiles > bot_tiles else -bot_tiles if usr_tiles < bot_tiles else 0)) / (usr_tiles + bot_tiles)
    f = (100.0 * (-usr_front_tiles if usr_front_tiles > bot_front_tiles else bot_front_tiles if usr_front_tiles < bot_front_tiles else 0)) / (usr_front_tiles + bot_front_tiles)

    # Popunjenost ćoškova
    usr_tiles = bot_tiles = 0
    for corner in CORNERS:
        if board[corner[0]][corner[1]] == USER:
            usr_tiles += 1
        elif board[corner[0]][corner[1]] == BOT:
            bot_tiles += 1
    c = 25 * (usr_tiles - bot_tiles)

    # Bliskost ćoškova
    usr_tiles = bot_tiles = 0
    for corner in CORNERS:
        if board[corner[0]][corner[1]] == EMPTY:
            for sub_corner in SUB_CORNERS:
                if board[sub_corner[0]][sub_corner[1]] == USER:
                    usr_tiles += 1
                elif board[sub_corner[0]][sub_corner[1]] == BOT:
                    bot_tiles += 1
    l = -12.5 * (usr_tiles - bot_tiles)

    # Mobilnost
    usr_tiles = len(get_moves(board, USER))
    bot_tiles = len(get_moves(board, BOT))
    m = (100.0 * (usr_tiles if usr_tiles > bot_tiles else -bot_tiles if usr_tiles < bot_tiles else 0)) / (usr_tiles + bot_tiles)

    # Finalna vrednost
    return (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
