import Piece
import Board
from Square import Square
import copy

#class Bishop(Piece):
class Bishop:
    def __init__(self):
        pass

    def do_move(start_square: Square, end_square: Square, board: Board):
        if Bishop.check_move_legal(start_square, end_square, board):
            board.unset_ep_square()
            end_square.piece = copy.deepcopy(start_square.piece)
            start_square.clear()

    def check_move_legal(start_square: Square, end_square: Square, board: Board):
        if not start_square.piece_stands():
            return False

        #if start_square.piece.name != "bishop":
        #    return False

        if board.move_order != start_square.piece.color:
            return False

        if (end_square.piece_stands()) and (start_square.piece.color == end_square.piece.color):
            return False

        if abs(start_square.rank - end_square.rank) != abs(ord(start_square.line) - ord(end_square.line)):
            return False

        move_direction = {'rank_sign': abs(start_square.rank - end_square.rank)//(end_square.rank - start_square.rank),
                          'line_sign': abs(ord(start_square.line) - ord(end_square.line))//(ord(end_square.line) - ord(start_square.line))}

        for rank_num in range(start_square.rank + move_direction['rank_sign'], end_square.rank, move_direction['rank_sign']):
            line = chr(ord(start_square.line) + move_direction['line_sign']*abs(rank_num - start_square.rank))
            if board.board[rank_num-1][ord(line) - ord("a")].piece_stands():
                return False

        return True

    def is_attacking(start_square: Square, end_square: Square, board: Board):

        if start_square == end_square:
            return False

        if abs(start_square.rank - end_square.rank) != abs(ord(start_square.line) - ord(end_square.line)):
            return False

        move_direction = {'rank_sign': abs(start_square.rank - end_square.rank)//(end_square.rank - start_square.rank),
                          'line_sign': abs(ord(start_square.line) - ord(end_square.line))//(ord(end_square.line) - ord(start_square.line))}

        for rank_num in range(start_square.rank + move_direction['rank_sign'], end_square.rank, move_direction['rank_sign']):
            line = chr(ord(start_square.line) + move_direction['line_sign']*abs(rank_num - start_square.rank))
            if board.board[rank_num-1][ord(line) - ord("a")].piece_stands():
                return False

        return True


if __name__ == "__main__":
    pass