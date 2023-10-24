import copy

import Piece
import Board
from Square import Square

class Rook:
    def __init__(self):
        pass

    def do_move(start_square: Square, end_square: Square, board: Board) -> None:
        if Rook.check_move_legal(start_square, end_square, board):
            board.unset_ep_square()
            if (start_square.short_description()[-2:]) == "a1" or (end_square.short_description()[-2:]) == "a1":
                board.castles.set_white_queenside_castle_impossible()

            if (start_square.short_description()[-2:]) == "a8" or (end_square.short_description()[-2:]) == "a8":
                board.castles.set_black_queenside_castle_impossible()

            if (start_square.short_description()[-2:]) == "h1" or (end_square.short_description()[-2:]) == "h1":
                board.castles.set_white_kingside_castle_impossible()

            if (start_square.short_description()[-2:]) == "h8" or (end_square.short_description()[-2:]) == "h8":
                board.castles.set_black_kingside_castle_impossible()
            end_square.piece = copy.deepcopy(start_square.piece)
            start_square.clear()


    def check_move_legal(start_square: Square, end_square: Square, board: Board):
        if not start_square.piece_stands():
            return False

        #if start_square.piece.name != "rook":
        #    return False

        if board.move_order != start_square.piece.color:
            return False

        if (end_square.piece_stands()) and (start_square.piece.color == end_square.piece.color):
            return False

        if (start_square.line != end_square.line) and (start_square.rank != end_square.rank):
            return False

        if start_square.rank == end_square.rank:
            move_direction = abs(ord(start_square.line) - ord(end_square.line))//(ord(end_square.line) - ord(start_square.line))
            for line_num in range(ord(start_square.line) - ord("a") + move_direction, ord(end_square.line) - ord("a"), move_direction):
                if board.board[start_square.rank-1][line_num].piece_stands():
                    return False

        if start_square.line == end_square.line:
            line_num = ord(start_square.line) - ord("a")
            move_direction = abs(start_square.rank - end_square.rank)//(end_square.rank - start_square.rank)
            for rank_num in range(start_square.rank + move_direction, end_square.rank, move_direction):
                if board.board[rank_num-1][line_num].piece_stands():
                    return False

        return True

    def is_attacking(start_square: Square, end_square: Square, board: Board):
        if start_square == end_square:
            return False

        if (start_square.line != end_square.line) and (start_square.rank != end_square.rank):
            return False

        if start_square.rank == end_square.rank:
            move_direction = abs(ord(start_square.line) - ord(end_square.line)) // (
                        ord(end_square.line) - ord(start_square.line))
            for line_num in range(ord(start_square.line) - ord("a") + move_direction, ord(end_square.line) - ord("a"),
                                  move_direction):
                if board.board[start_square.rank - 1][line_num].piece_stands():
                    return False

        if start_square.line == end_square.line:
            line_num = ord(start_square.line) - ord("a")
            move_direction = abs(start_square.rank - end_square.rank) // (end_square.rank - start_square.rank)
            for rank_num in range(start_square.rank + move_direction, end_square.rank, move_direction):
                if board.board[rank_num - 1][line_num].piece_stands():
                    return False

        return True


if __name__ == "__main__":
    pass