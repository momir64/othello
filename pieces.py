import random

EMPTY = 0
BLACK = 1
WHITE = 2
MOVES = 3

USER = BLACK if random.getrandbits(1) else WHITE
TRENUTNI = BLACK
BOT = WHITE if USER == BLACK else BLACK
