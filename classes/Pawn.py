from Square import Square
import Board
import copy

class Pawn:
    def __init__(self):
        pass

    def do_move(start_square: Square, end_square: Square, board: Board):
        if Pawn.check_move_legal(start_square, end_square, board):
            if abs(start_square.rank - end_square.rank) == 2:
                board.unset_ep_square()
                new_ep_square_rank = (start_square.rank + end_square.rank)//2
                board.set_ep_square(new_ep_square_rank, start_square.line)
                end_square.piece = copy.deepcopy(start_square.piece)
                start_square.clear()
                return ''

            if (abs(start_square.rank - end_square.rank)) == 1 and ((start_square.line == end_square.line)):
                board.unset_ep_square()
                end_square.piece = copy.deepcopy(start_square.piece)
                start_square.clear()
                return ''

            if (abs(start_square.rank - end_square.rank)) == 1 and ((start_square.line != end_square.line)) and (end_square.piece_stands()):
                board.unset_ep_square()
                end_square.piece = copy.deepcopy(start_square.piece)
                start_square.clear()
                return ''

            if (abs(start_square.rank - end_square.rank)) == 1 and ((start_square.line != end_square.line)) and (not end_square.piece_stands()):
                board.unset_ep_square()
                end_square.piece = copy.deepcopy(start_square.piece)
                start_square.clear()
                board.board[start_square.rank - 1][ord(end_square.line) - ord('a')].clear()
                if end_square.piece.color == 'w':
                    return str(end_square.rank - 2) + str(ord(end_square.line) - ord('a'))
                else:
                    return str(end_square.rank) + str(ord(end_square.line) - ord('a'))

            #CONSIDER PAWN PROMOTION AT SOME POINT

    def check_move_legal(start_square: Square, end_square: Square, board: Board):
        if not start_square.piece:
            return False

        if board.move_order != start_square.piece.color:
            return False

        legal = False

        if ((start_square.piece.color == 'w') and (start_square.line == end_square.line) and (start_square.rank + 1 == end_square.rank) and (not end_square.piece_stands())) or \
            ((start_square.piece.color == 'w') and (start_square.line == end_square.line) and (start_square.rank + 2 == end_square.rank) and (not end_square.piece_stands()) and \
             (not board.board[2][ord(start_square.line) - ord('a')].piece_stands()) and (start_square.rank == 2)):
            legal = True

        if ((start_square.piece.color == 'b') and (start_square.line == end_square.line) and (start_square.rank - 1 == end_square.rank) and (not end_square.piece_stands())) or \
            ((start_square.piece.color == 'b') and (start_square.line == end_square.line) and (start_square.rank - 2 == end_square.rank) and (not end_square.piece_stands()) and \
             (not board.board[5][ord(start_square.line) - ord('a')].piece_stands()) and (start_square.rank == 7)):
            legal = True

        if (start_square.piece.color == 'w') and (start_square.rank + 1 == end_square.rank) \
            and (abs(ord(start_square.line) - ord(end_square.line)) == 1) \
            and (((end_square.piece_stands()) and (end_square.piece.color != start_square.piece.color)) or \
                 (not end_square.piece_stands()) and (end_square.is_ep)):
            legal = True

        if (start_square.piece.color == 'b') and (start_square.rank - 1 == end_square.rank) \
            and (abs(ord(start_square.line) - ord(end_square.line)) == 1) \
            and (((end_square.piece_stands()) and (end_square.piece.color != start_square.piece.color)) or \
                 (not end_square.piece_stands()) and (end_square.is_ep)):
            legal = True

        return legal

        if legal:
            if start_square.rank == 7:
                piece = input("enter a piece to promote")

    def is_attacking(start_square: Square, end_square: Square, board: Board):
        return ((start_square.piece.color == 'w') and (start_square.rank + 1 == end_square.rank) and (abs(ord(start_square.line) - ord(end_square.line)) == 1)) or \
        ((start_square.piece.color == 'b') and (start_square.rank - 1 == end_square.rank) and (
                    abs(ord(start_square.line) - ord(end_square.line)) == 1))


if __name__ == "__main__":
    pass