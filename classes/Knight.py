import Piece
import Board
from Square import Square
import copy

class Knight:
    def __init__(self):
        pass

    def do_move(start_square: Square, end_square: Square, board: Board):
        if Knight.check_move_legal(start_square, end_square, board):
            board.unset_ep_square()
            end_square.piece = copy.deepcopy(start_square.piece)
            start_square.clear()

    def check_move_legal(start_square: Square, end_square: Square, board: Board):
        if not start_square.piece_stands():
            return False

        #if start_square.piece.name != "knight":
        #    return False

        if board.move_order != start_square.piece.color:
            return False

        if (end_square.piece_stands()) and (start_square.piece.color == end_square.piece.color):
            return False

        if (abs(start_square.rank - end_square.rank) + abs(ord(start_square.line) - ord(end_square.line)) == 3) and \
                (start_square.rank != end_square.rank) and (start_square.line != end_square.line):
            return True

        return False

    def is_attacking(start_square: Square, end_square: Square, board: Board):

        if (abs(start_square.rank - end_square.rank) + abs(ord(start_square.line) - ord(end_square.line)) == 3) and \
                (start_square.rank != end_square.rank) and (start_square.line != end_square.line):
            return True

        return False


if __name__ == "__main__":
    pass