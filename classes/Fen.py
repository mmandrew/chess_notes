import Board
import Square
import Consts


class Fen:
    def __init__(self, fen: str):
        self.fen = fen

    def parse_rank(self, rank: str, rank_num: int) -> [Square.Square]:
        Squares = []
        line = 'a'
        for c in rank:
            if c in ('1', '2', '3', '4', '5', '6', '7', '8'):
                for i in range(ord(c) - ord('0')):
                    Squares.append(Square.Square(line, rank_num))
                    line = chr(ord(line) + 1)
                continue
            if c in Consts.fen_shorts:
                piece, color = Consts.fen_shorts[c]
                Squares.append(Square.Square(line, rank_num, piece, color))
                line = chr(ord(line) + 1)
        return Squares

    def parse_board_part(self, board_part: str) -> [[Square.Square]]:
        board = []
        rank_parts = board_part.split('/')
        rank_parts.reverse()
        rank = 1
        for rank_part in rank_parts:
            board.append(self.parse_rank(rank_part, rank))
            rank += 1
        return board


    def fen_to_board(self) -> Board:
        [board, move_order, castles, ep] = self.fen.split(' ')[0:4]
        board = self.parse_board_part(board)
        new_board = Board.Board()
        new_board.set_custom_position(board, move_order, castles, ep)
        return new_board



