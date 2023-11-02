import copy

from Square import Square
from Castles import Castles
import Fen
from Move import Move
import Consts
from Piece import Piece
from tkinter import *
from PIL import ImageTk, Image
line_set = Consts.line_set

class Board:
    def __init__(self):
        self.board = []
        for rank in range(1,9):
            rank_squares = []
            for line in line_set:
                rank_squares.append(Square(line, rank))
            self.board.append(rank_squares)
        self.castles = Castles()
        self.move_order = 'w'
        self.ep_square = ''

    def copy_self(self):
        new_b = Board()

        for rank in range(8):
            for line in range(8):
                new_b.board[rank][line] = self.board[rank][line].copy_self()

        new_b.castles = copy.deepcopy(self.castles)
        new_b.move_order = self.move_order
        new_b.ep_square = self.ep_square

        return new_b

    def set_move_order(self, side: chr) -> None:
        if side in ['w', 'b']:
            self.move_order = side
        else:
            raise NameError("WRONG side")

    def flip_move_order(self):
        if self.move_order == 'w':
            self.move_order = 'b'
        else:
            self.move_order = 'w'

    def set_ep_square(self, *args) -> None:
        """
        *args for en passant square
        may be used like е5, 5e, Square(e, 5), (5, e), (e, 5) or just "-"
        """
        if not args[0] or args[0] == "-":
            return
        if (len(args) == 2) and (isinstance(args[0], int)) and (args[1] in Consts.line_set):
            self.board[args[0] - 1][ord(args[1]) - ord('a')].set_ep()
            #self.ep_square = self.board[args[0] - 1][ord(args[1]) - ord('a')]
            self.ep_square = args[1] + str(args[0])
            return

        if (len(args) == 2) and (isinstance(args[1], int)) and (args[0] in Consts.line_set):
            self.set_ep_square(args[1], args[0])

        if (len(args) == 1) and isinstance(args[0], Square):
            self.set_ep_square(Square.rank, Square.line)

        if (len(args) == 1) and (isinstance(args[0], str)):
            self.set_ep_square(args[0][0], int(args[0][1]))

    def unset_ep_square(self) -> None:
        ep = self.ep_square
        if (len(ep) == 2):
            self.board[int(ep[1]) - 1][ord(ep[0]) - ord('a')].unset_ep()
            self.ep_square

    def set_start_position(self):
        for square in self.board[1]:
            square.piece = Piece('pawn', 'w')
        for square in self.board[6]:
            square.piece = Piece('pawn', 'b')
        self.board[0][0].piece = self.board[0][7].piece = Piece('rook', 'w')
        self.board[0][1].piece = self.board[0][6].piece = Piece('knight', 'w')
        self.board[0][2].piece = self.board[0][5].piece = Piece('bishop', 'w')
        self.board[0][3].piece = Piece('queen', 'w')
        self.board[0][4].piece = Piece('king', 'w')
        self.board[7][0].piece = self.board[7][7].piece = Piece('rook', 'b')
        self.board[7][1].piece = self.board[7][6].piece = Piece('knight', 'b')
        self.board[7][2].piece = self.board[7][5].piece = Piece('bishop', 'b')
        self.board[7][3].piece = Piece('queen', 'b')
        self.board[7][4].piece = Piece('king', 'b')
        self.castles.set_castles_by_fen("KQkq")

        for line in self.board[2:6]:
            for square in line:
                square.clear()

        self.move_order = 'w'
        self.ep_square = None

    def square_attacked_by_white(self, square: Square) -> bool:
        for rank in self.board:
            for sq in rank:
                if (sq.piece) and (sq.piece.color == 'w'):
                    if Move.check_move_attacking(sq, square, self):
                        return True
        return False

    def square_attacked_by_black(self, square: Square) -> bool:
        for rank in self.board:
            for sq in rank:
                if (sq.piece) and (sq.piece.color == 'b'):
                    if Move.check_move_attacking(sq, square, self):
                        return True
        return False

    def white_king_in_check(self) -> bool:
        for rank in self.board:
            for square in rank:
                if (square.piece) and (square.piece.name == "king") and (square.piece.color == 'w'):
                    return self.square_attacked_by_black(square)

        print("No white king")
        return False

    def black_king_in_check(self) -> bool:
        for rank in self.board:
            for square in rank:
                if (square.piece) and (square.piece.name == "king") and (square.piece.color == 'b'):
                    return self.square_attacked_by_white(square)

        print("No black king")
        return False

    def king_in_illegal_check(self) -> bool:
        return ((self.move_order == 'w') and self.black_king_in_check()) or \
                ((self.move_order == 'b') and self.white_king_in_check())

    def king_in_check(self) -> bool:
        return ((self.move_order == 'b') and self.black_king_in_check()) or \
                ((self.move_order == 'w') and self.white_king_in_check())

    def king_in_stalemate(self) -> bool:
        return (not self.king_in_check()) and (self.king_in_mate())


    #def get_white_king_square(self):
    #    for rank in self.board:
    #        for square in rank:
    #            if (square.piece) and (square.piece.name == "king") and (square.piece.color == 'w'):
    #                return square

    #def get_black_king_square(self):
    #    for rank in self.board:
    #        for square in rank:
    #            if (square.piece) and (square.piece.name == "king") and (square.piece.color == 'b'):
    #                return square

    def king_in_mate(self) -> bool:
        for start_rank in self.board:
            for start_square in start_rank:
                if (start_square.piece_stands()) and (start_square.piece.color == self.move_order):
                    for end_rank in self.board:
                        for end_square in end_rank:
                            if Move.check_move_legal(start_square, end_square, self):
                                #start_square.print_square()
                                #end_square.print_square()
                                return False
        return True

    def set_custom_position(self, squares: [[Square]], move_order: chr, castles: str, *args) -> None:
        """
        *args for en passant square
        may be used like е5, 5e, Square(e, 5), (5, e), (e, 5)
        """
        for rank_num, rank in enumerate(squares):
            for line_num, square in enumerate(rank):
                self.board[rank_num][line_num] = square

        self.set_move_order(move_order)
        self.castles.set_castles_by_fen(castles)
        self.set_ep_square(*args)

    def board_to_fen(self) -> Fen:
        fen_board = ""
        for rank in reversed(self.board):
            rank_code = ""
            no_piece_counter = 0
            for square in rank:
                piece = square.piece
                if piece != '':
                    if no_piece_counter > 0:
                        rank_code += str(no_piece_counter)
                        no_piece_counter = 0
                    rank_code += Consts.piece_shorts[piece.name][piece.color]
                else:
                    no_piece_counter += 1
                    if square.line == 'h':
                        rank_code += str(no_piece_counter)
            fen_board += rank_code + "/"
        fen_board = fen_board[:-1] + ' '
        fen_board += self.move_order + ' '
        all_castles = ""
        if self.castles.white_kingside_castle_possible:
            all_castles += 'K'
        if self.castles.white_queenside_castle_possible:
            all_castles += 'Q'
        if self.castles.black_kingside_castle_possible:
            all_castles += 'k'
        if self.castles.black_queenside_castle_possible:
            all_castles += 'q'
        if not all_castles:
            all_castles = "-"
        fen_board += all_castles + ' '
        if self.ep_square:
            fen_board += self.ep_square.line + str(self.ep_square.rank)
        else:
            fen_board += '-'

        return fen_board

    def print_position_as_text_from_white(self):
        for rank in reversed(self.board):
            for square in rank:
                square.print_square()
            print()

    def print_position_as_text_from_black(self):
        for rank in self.board:
            for square in reversed(rank):
                square.print_square()
            print()

    def clear_board(self):
        for rank in self.board:
            for square in rank:
                square.clear()

    def simple_move(self, start_square:Square, end_square: Square):
        end_square.piece = start_square.piece
        start_square.clear()

    def white_kingside_castle(self):
        if self.castles.white_kingside_castle_possible:
            self.castles.set_white_kingside_castle_impossible()
            self.castles.set_white_queenside_castle_impossible()
            simple_move(self.board[0][4], self.board[0][6])
            simple_move(self.board[0][7], self.board[0][5])

    def white_queenside_castle(self):
        if self.castles.white_queenside_castle_possible:
            self.castles.set_white_queenside_castle_impossible()
            self.castles.set_white_kingside_castle_impossible()
            simple_move(self.board[0][4], self.board[0][2])
            simple_move(self.board[0][0], self.board[0][3])

    def black_kingside_castle(self):
        if self.castles.black_kingside_castle_possible():
            self.castles.set_black_kingside_castle_impossible()
            self.castles.set_black_queenside_castle_impossible()
            simple_move(self.board[7][4], self.board[7][6])
            simple_move(self.board[7][7], self.board[7][5])

    def black_queenside_castle(self):
        if self.castles.black_queenside_castle_possible:
            self.castles.set_black_kingside_castle_impossible()
            self.castles.set_black_queenside_castle_impossible()
            simple_move(self.board[7][4], self.board[7][2])
            simple_move(self.board[7][0], self.board[7][3])

    def make_move(self, start_square:Square, end_square: Square):
        pass

    def canvas_click_event(self, event):
        print('Clicked canvas: ', event.x, event.y, event.widget)

    def draw_empty_board(self):
        window = Tk()
        window.title("Chess notes")
        window.geometry("1200x605")

        canvas = Canvas(window, width = 600, height = 605)
        canvas.pack()
        img = ImageTk.PhotoImage(Image.open("../assets/board_image_1.png"))
        img_1 = ImageTk.PhotoImage(Image.open("../assets/queen_b.png"))
        b = canvas.create_image(300, 305, anchor = "center", image = img)
        q = canvas.create_image(280, 320, image = img_1)
        #canvas.bind('<Button-1>', self.canvas_click_event)
        canvas.tag_bind(q, '<Button-1>', self.canvas_click_event)
        window.mainloop()




    def draw_board(self):
        pass

    def move_piece(self, start_square, end_square):
        pass

if __name__ == "__main__":
    pass