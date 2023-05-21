class BoardHashMap:
    def __init__(self, size):
        self.table = [[] for _ in range(size)]
        self.size = size

    def to_bitboard(self, board):
        bitboard = 1
        for x in range(8):
            for y in range(8):
                bitboard = bitboard << 2 | board[x][y]
        return bitboard

    def add(self, board, val):
        key = self.to_bitboard(board)
        self.table[key % self.size].append((key, val))

    def get(self, board):
        key = self.to_bitboard(board)
        for item in self.table[key % self.size]:
            if item[0] == key:
                return item[1]
        return None
