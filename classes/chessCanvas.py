import os
import time
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
import Board
import Square
import Consts
import BoardSetup
import math
import Move
import Fen
import gameNotionField
import ast

class chessCanvas(tk.Tk):
    def __init__(self): #, window: Tk):
        board_image = []
        super().__init__()
        self.current_file_name = ""
        self.title("Chess notes")
        self.geometry("1250x655")
        self.update_idletasks()
        self.start_board = Board.Board()
        self.board = Board.Board()

        self.left_pad = 20
        self.right_pad = 593
        self.bottom_pad = 583
        self.top_pad =  10
        self.white_pieces_images = []
        self.black_pieces_images = []
        self.last_cursor_x = -1
        self.last_cursor_y = -1

        self.start_line = -1
        self.start_rank = -1
        self.end_line = -1
        self.end_rank = -1
        self.image_to_move = None

        self.board_reverted = False

        for i, piece in enumerate(Consts.piece_shorts):
            piece_img = ImageTk.PhotoImage(Image.open("../assets/{}_{}.png".format(piece, 'w')))
            self.white_pieces_images.append(piece_img)

            piece_img = ImageTk.PhotoImage(Image.open("../assets/{}_{}.png".format(piece, 'b')))
            self.black_pieces_images.append(piece_img)

        self.moves_frame = Frame(self, width=600)
        self.moves_frame.pack(side = LEFT)

        self.new_button = Button(self.moves_frame, text = "New", width = 91)
        self.new_button.update_idletasks() ##???
        self.new_button.pack(side = TOP)
        self.new_button.bind("<Button-1>", self.create_new_setup)

        #self.pgn_text = Text(self.moves_frame)
        self.pgn_text = gameNotionField.gameNotionField(self.start_board, self.moves_frame, width=78)
        self.pgn_text.bind("<Button-1>", self.go_to_move)
        self.pgn_text.pack(side = TOP)

        self.save_button = Button(self.moves_frame, text = "Save", width = 45, command = self.save_chess_tree)
        self.save_button.pack(side = LEFT)
        self.save_button.bind("<Button-1>", self.save_chess_tree)

        self.load_button = Button(self.moves_frame, text = "Load", width = 45, command = self.load_chess_tree)
        self.load_button.pack(side = RIGHT)

        self.board_frame = Frame(self)
        self.board_frame.pack(side = RIGHT)

        self.canvas = Canvas(self.board_frame, width = self.winfo_width() // 2, height = 605)
        self.canvas.bind('<Button-1>', self.canvas_tapped)
        self.canvas.bind('<ButtonRelease>', self.canvas_untapped)
        self.canvas.pack()

        self.board_img = ImageTk.PhotoImage(Image.open("../assets/board_image_1.png"))
        self.board_id = self.canvas.create_image(300, 305, anchor = "center", image = self.board_img)

        self.full_back_image = ImageTk.PhotoImage(Image.open("../assets/full_back.png"))
        self.full_back_button = Button(self.board_frame, width = 129, height= 50, image = self.full_back_image)
        self.full_back_button.pack(side = LEFT)

        self.back_image = ImageTk.PhotoImage(Image.open("../assets/back.png"))
        self.back_button = Button(self.board_frame, width = 129, height= 50, image = self.back_image)
        self.back_button.pack(side = LEFT)

        self.flip_board_image = ImageTk.PhotoImage(Image.open("../assets/flip_board_arrow.png"))
        self.flip_board_button = Button(self.board_frame, width = 60, heigh = 50, image = self.flip_board_image)
        self.flip_board_button.bind('<Button-1>', self.flip_board_and_pieces)
        self.flip_board_button.pack(side = LEFT)

        self.move_image = ImageTk.PhotoImage(Image.open("../assets/move.png"))
        self.move_button = Button(self.board_frame, width = 129, height= 50, image = self.move_image)
        self.move_button.pack(side = LEFT)

        self.full_move_image = ImageTk.PhotoImage(Image.open("../assets/full_move.png"))
        self.full_move_button = Button(self.board_frame, width = 129, height= 50, image = self.full_move_image)
        self.full_move_button.pack(side = LEFT)

    def flip_board_and_pieces(self, event):
        self.flip_board()
        self.reverse_all_pieces()

    def change_board_image(self, img_path):
        self.canvas.delete(self.board_id)
        self.board_img = ImageTk.PhotoImage(Image.open(img_path))
        self.board_id = self.canvas.create_image(300, 305, anchor = 'center', image = self.board_img)

    def flip_board(self):
        if not self.board_reverted:
            self.change_board_image("../assets/board_revert.png")
            self.board_reverted = True
        else:
            self.change_board_image("../assets/board_image_1.png")
            self.board_reverted = False

    def reverse_all_pieces(self):
        for rank in self.board.board:
            for square in rank:
                self.reverse_piece_image(square)

    def reverse_piece_image(self, square: Square):
        if not square.piece_stands():
            return

        #delete old image
        piece_img = square.piece_img
        self.canvas.delete(square.canvas_id)

        #get axises by square line and rank
        line = ord(square.line) - ord('a')
        rank = square.rank - 1
        x_center, y_center = self.get_square_center_by_line_rank(line, rank)

        #create new on new axises
        square.canvas_id = self.canvas.create_image(x_center, y_center, anchor = 'center', image = piece_img)
        square.piece_img = piece_img

    def get_square_center(self, x, y):
        half_square = (self.bottom_pad - self.top_pad) / 16
        sqaure_side = self.calc_square_size()
        x_center = self.left_pad + half_square + sqaure_side * int((x - self.left_pad) / sqaure_side)
        y_center = self.top_pad +half_square + sqaure_side * int((y - self.top_pad) / sqaure_side)
        return x_center, y_center

    def get_square_axises(self, x, y):
        square_size = self.calc_square_size()
        x_axis = math.floor((x - self.left_pad) / square_size)
        y_axis = math.floor((y - self.top_pad) / square_size)
        if not self.board_reverted:
            return x_axis, 7 - y_axis #line, rank
        else:
            return 7 - x_axis, y_axis #?

    def move_piece_img(self, start_rank, start_line, end_rank, end_line):

        start_square = self.board.board[start_rank][start_line]
        end_square = self.board.board[end_rank][end_line]

        self.clear_canvas_square(end_square)
        end_square.piece_img = start_square.piece_img
        x_center, y_center = self.get_square_center_by_line_rank(end_line, end_rank)
        end_square.canvas_id = self.canvas.create_image(x_center, y_center, anchor="center", image=end_square.piece_img)

        self.clear_canvas_square(start_square)

    def canvas_tapped(self, event):
        if not (self.top_pad < event.y < self.bottom_pad) or not (self.left_pad < event.x < self.right_pad):
            return

        x_center, y_center = self.get_square_center(event.x, event.y)
        line, rank = self.get_square_axises(x_center, y_center)
        considered_square = self.board.board[rank][line]

        if not considered_square.piece_stands():
            return

        self.last_cursor_x = event.x
        self.last_cursor_y = event.y

        self.start_line = line
        self.start_rank = rank
        self.image_to_move = considered_square.piece_img

    def process_comment_from_move(self, comment):
        if len(comment) == 0:
            return

        if len(comment) == 2:
            rank = int(comment[0])
            line = int(comment[1])
            self.clear_canvas_square(self.board.board[rank][line])
            return

        if len(comment) == 4:
            start_rank = int(comment[0])
            start_line = int(comment[1])
            end_rank = int(comment[2])
            end_line = int(comment[3])
            self.move_piece_img(start_rank, start_line, end_rank, end_line)

    def go_to_move(self, event):
        board_to_set = self.pgn_text.go_to_move(event)
        self.full_board_clear()
        self.board = board_to_set.copy_self()
        self.draw_pieces()

    def canvas_untapped(self, event):
        if not (self.top_pad < event.y < self.bottom_pad) or not (self.left_pad < event.x < self.right_pad):
            return

        x_center, y_center = self.get_square_center(event.x, event.y)
        line, rank = self.get_square_axises(x_center, y_center)
        start_square = self.board.board[self.start_rank][self.start_line]

        considered_square = self.board.board[rank][line]

        self.end_rank = rank
        self.end_line = line

        end_square = self.board.board[self.end_rank][self.end_line]

        if Move.Move.check_move_legal(start_square, end_square, self.board):
            self.board, comment, move_note = Move.Move.do_move(start_square, end_square, self.board)
            print(move_note)
            print(self.pgn_text.current_move)
            self.pgn_text.record_a_move(move_note, self.board.board_to_fen())

            self.move_piece_img(self.start_rank, self.start_line, self.end_rank, self.end_line)
            self.process_comment_from_move(comment)
        else:
            print("Ilegal")
            self.start_line = self.end_line = self.start_rank = self.end_rank = -1
        print(self.board.king_in_mate())

    """
    def actualize(self):
        self.draw_pieces()
    """

    """
    def actualize_board_look_to(self, board: Board.Board):
        for rank in range(8):
            for line in range(8):
                target_square = board.board[rank][line]
                current_square = self.board.board[rank][line]
                target_square.print_square()
                current_square.print_square()
                if not target_square.piece_stands():
                    #current_square.print_square()
                    print(current_square.canvas_id, end=' ')
                    self.clear_canvas_square(current_square)
                    print(current_square.canvas_id, end=' ')
                    print("HERE ", end='')
                    target_square.print_square()
                    current_square.print_square()
                    continue
                x_center, y_center = self.get_square_center_by_line_rank(line, rank)

                if target_square.piece.color == 'w':
                    img_to_put = self.white_pieces_images[Consts.piece_set.index(target_square.piece.name)]
                else:
                    img_to_put = self.black_pieces_images[Consts.piece_set.index(target_square.piece.name)]

                print(current_square.canvas_id, end=' ')
                current_square.canvas_id = self.canvas.create_image(x_center, y_center, anchor="center", image=img_to_put)
                print(current_square.canvas_id, end='')
                current_square.piece_img = img_to_put
                target_square.print_square()
                current_square.print_square()
    """

    """
    def actualize_board_look(self):
        for rank in range(8):
            for line in range(8):
                square = self.board.board[rank][line]
                if not square.piece_stands():
                    square.print_square()

                    #if square.canvas_id > 0:
                    #    self.canvas.delete(square.canvas_id)
                    #    square.piece_img = None
                    self.clear_canvas_square(square)
                    continue
                x_center, y_center = self.get_square_center_by_line_rank(line, rank)

                if square.piece.color == 'w':
                    img_to_put = self.white_pieces_images[Consts.piece_set.index(square.piece.name)]
                else:
                    img_to_put = self.black_pieces_images[Consts.piece_set.index(square.piece.name)]

                square.canvas_id = self.canvas.create_image(x_center, y_center, anchor="center", image=img_to_put)
                square.piece_img = img_to_put
    """

    def open_setup_window(self):
        setup_window = BoardSetup.board_set(self, self.board)
        self.wait_window(setup_window)
        self.start_board = self.board.copy_self()
        self.pgn_text.set_start_board(self.start_board)

        return setup_window.board_reverted

    def calc_square_size(self):
        return (self.bottom_pad - self.top_pad) / 8

    def get_square_center_by_line_rank(self, line, rank):
        half_square = (self.bottom_pad - self.top_pad) / 16
        sqaure_side = self.calc_square_size()
        if not self.board_reverted:
            x_center = self.left_pad + half_square + sqaure_side * line
            y_center = self.top_pad + half_square + sqaure_side * (7 - rank)
        else:
            x_center = self.left_pad + half_square + sqaure_side * (7 - line)
            y_center = self.top_pad + half_square + sqaure_side * rank

        return x_center, y_center

    def clear_canvas_square(self, square: Square.Square):
        self.canvas.delete(square.canvas_id)
        square.canvas_id = 0
        square.piece_img = None

    def draw_piece_on_square(self, square: Square):
        if not square.piece_stands():
            self.clear_canvas_square(square)
            return

        if square.piece.color == 'w':
            img_to_put = self.white_pieces_images[Consts.piece_set.index(square.piece.name)]
        else:
            img_to_put = self.black_pieces_images[Consts.piece_set.index(square.piece.name)]

        line = ord(square.line) - ord('a')
        rank = square.rank - 1
        x_center, y_center = self.get_square_center_by_line_rank(line, rank)
        square.canvas_id = self.canvas.create_image(x_center, y_center, anchor = 'center', image = img_to_put)
        square.piece_img = img_to_put

    def draw_pieces(self):
        for rank in self.board.board:
            for square in rank:
                self.draw_piece_on_square(square)

    def full_board_clear(self):
        for rank in self.board.board:
            for square in rank:
                square.clear()
                self.clear_canvas_square(square)

    def clear_pgn(self):
        self.pgn_text.clear()

    def create_new_setup(self, event):
        board_reverted = self.open_setup_window()
        self.draw_pieces()
        if board_reverted and not self.board_reverted:
            self.change_board_image("../assets/board_revert.png")
            self.board_reverted = True
            self.reverse_all_pieces()

        if (not board_reverted and self.board_reverted):
            self.change_board_image("../assets/board_image_1.png")
            self.board_reverted = False
            self.reverse_all_pieces()

        return "break"

    def save_chess_tree(self, event):
        path = filedialog.asksaveasfilename(initialfile= "Untitled", defaultextension='.txt', filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if path:
            lines_to_save = self.pgn_text.lines
            fens_to_save = self.pgn_text.lines_and_fens
            with open(path, 'w+') as f:
                for line in lines_to_save:
                    f.write(line + '\n')
                f.write("LINES AND FENES\n")
                for line in fens_to_save:
                    f.write(str(line) + '\n')
        return "break"

    def load_chess_tree(self):
        path = filedialog.askopenfile(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if path:
            print(path.name)
            with open(path.name, 'r') as f:
                lines = [line[:-1] for line in path.readlines()]
                fens_border = lines.index("LINES AND FENES")
                self.pgn_text.lines = lines[:fens_border]
                self.pgn_text.lines_and_fens = []
                for line in lines[fens_border+1:]:
                    self.pgn_text.lines_and_fens.append(ast.literal_eval(line))
                print("FENS")
                print(self.pgn_text.lines_and_fens)
                self.pgn_text.update_text_by_lines()

                fen_to_set = Fen.Fen(self.pgn_text.lines_and_fens[0][0]["fen"])
                board_to_set = fen_to_set.fen_to_board()

                self.start_board = board_to_set.copy_self()
                #self.board = board_to_set.copy_self()

                self.pgn_text.set_start_board(self.start_board)

                self.full_board_clear()
                self.board = board_to_set.copy_self()
                self.draw_pieces()
            print(lines)
        else:
            print("No file")

    def full_back(self):
        pass

    """
    def draw_piece_on_board(self, piece_short: chr, square: Square) -> None:
        self.canvas.pack()
        png_path = os.path.join(os.getcwd(), "..\\assets\{}_{}.png".format(square.piece.name, square.piece.color))
        piece_img = ImageTk.PhotoImage(Image.open(png_path))
        #b = canvas.create_image(300, 305, anchor = "center", image = img)
        img = ImageTk.PhotoImage(Image.open("../assets/board_image_1.png"))
        b = self.canvas.create_image(300, 305, anchor = "center", image = img)
        x_axis = (self.canvas.winfo_width()) * (1 + 2 * (square.rank - 1)) // 16
        y_axis = (self.canvas.winfo_height()) * (1 + 2 * (ord(square.line) - ord('a'))) // 16
        q = self.canvas.create_image(x_axis, y_axis, anchor = "center", image = img)
    """

    """
    def draw_empty_board(self):
        self.canvas.pack()
        img = ImageTk.PhotoImage(Image.open("../assets/board_image_1.png"))
        b = self.canvas.create_image(300, 305, anchor = "center", image = img)
        self.mainloop()
    """

    def draw_board(self, board):
        for rank in self.board.board:
            for square in rank:
                pass

    def move_forward(self):
        pass

    def move_back(self):
        pass


if __name__ == "__main__":
    pass
