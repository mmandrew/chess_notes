from Square import Square
from Bishop import Bishop
from Knight import Knight
from Rook import Rook
from Queen import Queen
from King import King
import Board
from Pawn import Pawn
import copy
import Consts
class Move:
    def __init__(self, start_square: Square, end_square: Square):
        self.start_square = start_square
        self.end_square = end_square

    def simple_move(start_square: Square, end_square: Square, board: Board):
        end_square.piece = copy.deepcopy(start_square.piece)
        start_square.clear()
        board.flip_move_order()

    def check_king_wont_be_in_check(start_square: Square, end_square: Square, board: Board) -> bool:
        board_after = board.copy_self()
        start_square_after = board_after.board[start_square.rank - 1][ord(start_square.line) - ord('a')]
        end_square_after = board_after.board[end_square.rank - 1][ord(end_square.line) - ord('a')]
        Move.simple_move(start_square_after, end_square_after, board_after)
        return (not board_after.king_in_illegal_check())

    def king_would_be_in_mate(start_square: Square, end_square: Square, board: Board) -> bool:
        board_after = board.copy_self()
        start_square_after = board_after.board[start_square.rank - 1][ord(start_square.line) - ord('a')]
        end_square_after = board_after.board[end_square.rank - 1][ord(end_square.line) - ord('a')]
        Move.simple_move(start_square_after, end_square_after, board_after)
        return board_after.king_in_mate()

    def king_would_be_in_check(start_square: Square, end_square: Square, board: Board) -> bool:
        board_after = board.copy_self()
        start_square_after = board_after.board[start_square.rank - 1][ord(start_square.line) - ord('a')]
        end_square_after = board_after.board[end_square.rank - 1][ord(end_square.line) - ord('a')]
        Move.simple_move(start_square_after, end_square_after, board_after)
        return board_after.king_in_check()

    def king_would_be_in_stalemate(self):
        pass

    def note_on_move(start_square: Square, end_square: Square, board: Board) -> str:
        if (start_square.piece.name == 'king') and (start_square.line == 'e') and (end_square.line == 'g'):
            move_note = 'O-O'
        elif (start_square.piece.name == 'king') and (start_square.line == 'e') and (end_square.line == 'c'):
            move_note = 'O-O-O'
        else:
            move_note = ''

            if not start_square.piece.name == 'pawn':
                move_note = Consts.piece_shorts[start_square.piece.name]['w']

            move_note += start_square.line + str(start_square.rank)

            if (end_square.piece_stands()) or ((start_square.piece.name == 'pawn') and (not start_square.line == end_square.line)):
                move_note += ':'
            else:
                move_note += '-'

            move_note += end_square.line + str(end_square.rank)

        return move_note

    def do_move(start_square: Square, end_square: Square, board: Board) -> Board:
        comment = ''
        move_note = ''
        if Move.check_move_legal(start_square, end_square, board):
            move_note = Move.note_on_move(start_square, end_square, board)
            if start_square.piece.name == 'pawn':
                comment = Pawn.do_move(start_square, end_square, board)
            if start_square.piece.name == 'knight':
                Knight.do_move(start_square, end_square, board)
            if start_square.piece.name == 'bishop':
                Bishop.do_move(start_square, end_square, board)
            if start_square.piece.name == 'rook':
                move = Rook.do_move(start_square, end_square, board)
            if start_square.piece.name == 'queen':
                Queen.do_move(start_square, end_square, board)
            if start_square.piece.name == 'king':
                comment = King.do_move(start_square, end_square, board)
            board.flip_move_order()

            if board.king_in_mate():
                move_note += 'x'
                return board, comment, move_note

            if board.king_in_check():
                move_note += '+'
                return board, comment, move_note

        return board, comment, move_note


    def check_move_legal(start_square: Square, end_square: Square, board: Board):
        if start_square == end_square:
            return False

        if not start_square.piece_stands():
            return False

        if start_square.piece.name == 'knight':
            return Knight.check_move_legal(start_square, end_square, board) and Move.check_king_wont_be_in_check(start_square, end_square, board)
        if start_square.piece.name == 'bishop':
            return Bishop.check_move_legal(start_square, end_square, board) and Move.check_king_wont_be_in_check(start_square, end_square, board)
        if start_square.piece.name == 'rook':
            return Rook.check_move_legal(start_square, end_square, board) and Move.check_king_wont_be_in_check(start_square, end_square, board)
        if start_square.piece.name == 'queen':
            return Queen.check_move_legal(start_square, end_square, board) and Move.check_king_wont_be_in_check(start_square, end_square, board)
        if start_square.piece.name == 'pawn':
            return Pawn.check_move_legal(start_square, end_square, board) and Move.check_king_wont_be_in_check(start_square, end_square, board)
        if start_square.piece.name == 'king':
            return King.check_move_legal(start_square, end_square, board) and Move.check_king_wont_be_in_check(start_square, end_square, board)

    def check_move_attacking(start_square: Square, end_square: Square, board: Board) -> bool:
        if not start_square.piece:
            return False

        if start_square.piece.name == 'knight':
            return Knight.is_attacking(start_square, end_square, board)
        if start_square.piece.name == 'bishop':
            return Bishop.is_attacking(start_square, end_square, board)
        if start_square.piece.name == 'rook':
            return Rook.is_attacking(start_square, end_square, board)
        if start_square.piece.name == 'queen':
            return Queen.is_attacking(start_square, end_square, board)
        if start_square.piece.name == 'pawn':
            return Pawn.is_attacking(start_square, end_square, board)
        if start_square.piece.name == 'king':
            return King.is_attacking(start_square, end_square, board)

    def take_a_piece(self):
        pass

    #def castle_legal(self, board: Board):
    #    return (self.start_square.print_square() == "Ke1") and \
    #        (self.end_square.print_square() == "g1") and \
    #        (board.castles.white_kingside_castle_possible) and \
    #        (not board.square_attacked_by_black(board[0][5])) and \
    #        (not board.square_attacked_by_black(board[0][4]))

    #def en_passan(self):
    #    pass

    def pawn_promotion(self):
        pass

    def move_note(self):
        pass

    def make_move(self):
        pass


if __name__ == "__main__":
    pass
