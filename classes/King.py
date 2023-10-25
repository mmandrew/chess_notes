from Square import Square
import Board
import Move
import copy

class King:
    def __init__(self):
        pass

    def do_move(start_square: Square, end_square: Square, board: Board) -> None:
        if King.check_move_legal(start_square, end_square, board):
            board.unset_ep_square()
            if start_square.piece.color == 'w':
                board.castles.set_white_queenside_castle_impossible()
                board.castles.set_white_kingside_castle_impossible()
            else:
                board.castles.set_black_kingside_castle_impossible()
                board.castles.set_black_queenside_castle_impossible()

            if (abs(start_square.rank - end_square.rank) <= 1) and (abs(ord(start_square.line) - ord(end_square.line)) <= 1):
                end_square.piece = copy.deepcopy(start_square.piece)
                start_square.clear()
                return ''

            if (start_square.short_description() == "Ke1") and (end_square.short_description() == "g1"):
                end_square.piece = copy.deepcopy(start_square.piece)
                start_square.clear()
                board.board[0][5].piece = board.board[0][7].piece.copy_self()
                board.board[0][7].clear()
                return '0705'

            if (start_square.short_description() == "Ke1") and (end_square.short_description() == "c1"):
                end_square.piece = copy.deepcopy(start_square.piece)
                start_square.clear()
                board.board[0][3].piece = board.board[0][0].piece.copy_self()
                board.board[0][0].clear()
                return '0003'

            if (start_square.short_description() == "ke8") and (end_square.short_description() == "g8"):
                end_square.piece = copy.deepcopy(start_square.piece)
                start_square.clear()
                board.board[7][5].piece = board.board[7][7].piece.copy_self()
                board.board[7][7].clear()
                return '7775'

            if (start_square.short_description() == "ke8") and (end_square.short_description() == "c8"):
                end_square.piece = copy.deepcopy(start_square.piece)
                start_square.clear()
                board.board[7][3].piece = board.board[7][0].piece.copy_self()
                board.board[7][0].clear()
                return '7073'

    def check_move_legal(start_square: Square, end_square: Square, board: Board):
        if board.move_order != start_square.piece.color:
            return False

        if (end_square.piece_stands()) and (start_square.piece.color == end_square.piece.color):
            return False

        if (abs(start_square.rank - end_square.rank) <= 1) and (abs(ord(start_square.line) - ord(end_square.line)) <= 1):
            return ((start_square.piece.color == "w") and (not board.square_attacked_by_black(end_square))) or \
                ((start_square.piece.color == "b") and (not board.square_attacked_by_white(end_square)))

        if (start_square.short_description() == "Ke1") and \
            (end_square.short_description() == "g1") and \
            (board.castles.white_kingside_castle_possible) and \
            (not board.square_attacked_by_black(board.board[0][6])) and \
            (not board.square_attacked_by_black(board.board[0][5])) and \
            (not board.square_attacked_by_black(board.board[0][4])) and \
            (not board.board[0][5].piece_stands()) and \
            (not end_square.piece_stands()):
            return True

        if (start_square.short_description() == "Ke1") and \
            (end_square.short_description() == "c1") and \
            (board.castles.white_queenside_castle_possible) and \
            (not board.square_attacked_by_black(board.board[0][2])) and \
            (not board.square_attacked_by_black(board.board[0][3])) and \
            (not board.square_attacked_by_black(board.board[0][4])) and \
            (not board.board[0][3].piece_stands()) and \
            (not end_square.piece_stands()) and \
            (not board.board[0][1].piece_stands()):
            return True

        if (start_square.short_description() == "ke8") and \
            (end_square.short_description() == "g8") and \
            (board.castles.black_kingside_castle_possible) and \
            (not board.square_attacked_by_white(board.board[7][6])) and \
            (not board.square_attacked_by_white(board.board[7][5])) and \
            (not board.square_attacked_by_white(board.board[7][4])) and \
            (not board.board[7][5].piece_stands()) and \
            (not end_square.piece_stands()):
            return True

        if (start_square.short_description() == "ke8") and \
            (end_square.short_description() == "c8") and \
            (board.castles.black_queenside_castle_possible) and \
            (not board.square_attacked_by_white(board.board[7][2])) and \
            (not board.square_attacked_by_white(board.board[7][3])) and \
            (not board.square_attacked_by_white(board.board[7][4])) and \
            (not board.board[7][3].piece_stands()) and \
            (not end_square.piece_stands()) and \
            (not board.board[7][1].piece_stands()):
            return True

        return False

    def is_attacking(start_square: Square, end_square: Square, board: Board):
        if start_square == end_square:
            return False

        return (abs(start_square.rank - end_square.rank) <= 1) and (abs(ord(start_square.line) - ord(end_square.line)) <= 1)


if __name__ == "__main__":
    pass