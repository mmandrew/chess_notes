import Piece
import Board
from Square import Square
from Bishop import Bishop
from Rook import Rook
import copy

class Queen:
    def __init__(self):
        pass

    def do_move(start_square: Square, end_square: Square, board: Board):
        if Queen.check_move_legal(start_square, end_square, board):
            board.unset_ep_square()
            end_square.piece = copy.deepcopy(start_square.piece)
            start_square.clear()

    def check_move_legal(start_square: Square, end_square: Square, board: Board):
        return (Bishop.check_move_legal(start_square, end_square, board) or
            Rook.check_move_legal(start_square, end_square, board))

    def is_attacking(start_square: Square, end_square: Square, board: Board):
        if start_square == end_square:
            return False

        return(Bishop.is_attacking(start_square, end_square, board) or Rook.is_attacking(start_square, end_square, board))


if __name__ == "__main__":
    pass