import Consts
import Piece
import copy

class Square:
    def __init__(self, line: chr, rank: int, *args):
        """
        *args may be Piece example or like ('bishop', 'w')
        """
        if (rank in range(1,9)) and (line in Consts.line_set):
            self.rank = rank
            self.line = line
        else:
            raise NameError("incorrect line or rank")
        if (rank - 1 + ord(line) - ord('a')) % 2 == 0:
            self.color = 'B'
        else:
            self.color = 'W'
        if len(args) == 2:
            self.set_piece(Piece.Piece(args[0], args[1]))
        if len(args) == 1 and isinstance(args[0], Piece.Piece):
            self.set_piece(args[0])
        if len(args) == 0:
            #self.piece = None
            self.piece = Piece.Piece('', '')
        self.is_ep = False
        self.canvas_id = 0
        self.piece_img = None

    def copy_self(self):
        new_s = Square(self.line, self.rank)
        #new_s.color = self.color
        new_s.piece = self.piece.copy_self()
        new_s.is_ep = self.is_ep
        new_s.canvas_id = 0
        new_s.piece_img = None

        return new_s

    def piece_stands(self):
        return not self.piece.name == ''

    def short_description(self) -> str:
        sd = ""
        if self.piece_stands():
            sd = Consts.piece_shorts[self.piece.name][self.piece.color]

        sd += self.line + str(self.rank)

        if self.is_ep:
            sd += "ep"

        return sd

    def set_ep(self):
        self.is_ep = True

    def unset_ep(self):
        self.is_ep = False

    def set_piece(self, piece: Piece.Piece):
        if piece.name in Consts.piece_set:
            self.piece = piece
            #self.piece = copy.deepcopy(piece)
        else:
            raise NameError("WRONG piece name - {}".format(piece))

    def print_square(self):
        print(self.short_description() + ' ', end="")

    def clear(self):
        self.piece = Piece.Piece('', '')

if __name__ == "__main__":
    pass
