class BoardHashMap:
    def __init__(self, size):
        self.table = [[] for _ in range(size)]
        self.size = size

    # pretvara stanje table i prosleđenu dubinu u jedinstvenu celobrojnu vrednost
    # dubina se koristi kod transpozicione tabele
    def to_bitboard(self, board, depth):
        bitboard = depth
        for x in range(8):
            for y in range(8):
                bitboard = bitboard << 2 | board[x][y]
        return bitboard

    # dodaje val u hash tabelu
    def add(self, board, val, depth=1):
        key = self.to_bitboard(board, depth)
        self.table[key % self.size].append((key, val))

    # vraća val iz hash tabele ukoliko postoji, u suprotnom vraća None
    def get(self, board, depth=1):
        key = self.to_bitboard(board, depth)
        for item in self.table[key % self.size]:
            if item[0] == key:
                return item[1]
        return None
