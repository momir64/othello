from datetime import datetime
from game_logic import *
from hashmap import *
from globals import *

# podešavanja
MAX_DEPTH = 15
MAX_DEPTH_TIME = 2  # sekundi
PRIME_SIZE = 1000003
HEURISTIC_MAP = BoardHashMap(PRIME_SIZE)
TRANSPOSITION_MAP = BoardHashMap(PRIME_SIZE)
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

# pomoćna funkcija
def calc_function(usr, bot, sign):
    if usr > bot:
        return sign * 100.0 * usr / (usr + bot)
    elif usr < bot:
        return -1 * sign * 100.0 * bot / (usr + bot)
    else:
        return 0

# funkcija koja računa heuristiku i koristi hash tabelu za čuvanje i čitanje već izračunatih
def heuristic_function(board):
    score = HEURISTIC_MAP.get(board)
    if score:
        return score

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

    # Količina
    p = calc_function(usr_tiles, bot_tiles, 1)

    # Stabilnost
    f = calc_function(usr_front_tiles, bot_front_tiles, -1)

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
    for i, corner in enumerate(CORNERS):
        if board[corner[0]][corner[1]] == EMPTY:
            for sub_corner in SUB_CORNERS[i]:
                if board[sub_corner[0]][sub_corner[1]] == USER:
                    usr_tiles += 1
                elif board[sub_corner[0]][sub_corner[1]] == BOT:
                    bot_tiles += 1
    l = -12.5 * (usr_tiles - bot_tiles)

    # Mobilnost
    m = calc_function(len(get_moves(board, USER)), len(get_moves(board, BOT)), 1)

    # Finalna vrednost
    score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
    HEURISTIC_MAP.add(board, score)
    return score

# minimax funkcija sa alpha-beta rezovima, tabelom transpozicija i vremenskim ograničenjem
def minimax(board, trenutni, depth, alpha, beta, start_time):
    result = TRANSPOSITION_MAP.get(board, depth)
    if result:
        return result

    if (datetime.now() - start_time).total_seconds() >= MAX_DEPTH_TIME:
        return None

    moves = get_moves(board, trenutni)
    if not depth or not moves:
        return heuristic_function(board), None

    score = -float('inf') if trenutni == USER else float('inf')
    for move in moves:
        tmp_board = [r[:] for r in board]
        flip(tmp_board, trenutni, move[0], move[1])
        minimax_result = minimax(tmp_board, switch_trenutni(trenutni), depth - 1, alpha, beta, start_time)
        if not minimax_result:
            return None
        minimax_score = minimax_result[0]
        if trenutni == USER:
            score = max(score, minimax_score)
            alpha = max(alpha, minimax_score)
        else:
            score = min(score, minimax_score)
            beta = min(beta, minimax_score)
        if beta <= alpha:
            break

    TRANSPOSITION_MAP.add(board, (score, move), depth)
    return score, move

# traženje najboljeg poteza sa vremenskim ograničenjem (iterative deepening)
def make_move(board):
    depth = 1
    result = True
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < MAX_DEPTH_TIME and result and depth <= MAX_DEPTH:
        result = minimax(board, BOT, depth, -float('inf'), float('inf'), start_time)
        if result:
            move = result[1]
        depth += 1
    return move
