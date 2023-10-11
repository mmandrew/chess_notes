piece_set = ('pawn', 'knight', 'bishop', 'rook', 'queen', 'king', '')
color_set = ('w', 'b', '')
line_set = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
fen_shorts = {'p': ['pawn', 'b'], 'n': ['knight', 'b'], 'b': ['bishop', 'b'], 'r': ['rook', 'b'], 'q': ['queen', 'b'], 'k': ['king', 'b'],
              'P': ['pawn', 'w'], 'N': ['knight', 'w'], 'B': ['bishop', 'w'], 'R': ['rook', 'w'], 'Q': ['queen', 'w'], 'K': ['king', 'w']}
piece_shorts = {'pawn': {'w': 'P', 'b': 'p'}, 'knight': {'w': 'N', 'b': 'n'}, 'bishop': {'w': 'B', 'b': 'b'},
                'rook': {'w': 'R', 'b': 'r'}, 'queen': {'w': 'Q', 'b': 'q'}, 'king': {'w': 'K', 'b': 'k'}}

def get_file_by_fen_short(fen_short: chr):
    l = fen_shorts[fen_short]
    return "{}_{}".format(l[0], l[1])

if __name__ == "__main__":
    pass