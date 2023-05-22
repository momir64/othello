import random

EMPTY = 0
BLACK = 1
WHITE = 2
MOVES = 3

# random određivanje da li korisnik igra prvi ili drugi
# prvi igrač je uvek crni
USER = BLACK if random.getrandbits(1) else WHITE
BOT = WHITE if USER == BLACK else BLACK
