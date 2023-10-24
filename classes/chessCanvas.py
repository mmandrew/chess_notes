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

class chessCanvas(tk.Tk):
    def __init__(self): #, window: Tk):
        board_image = []
        super().__init__()
        self.current_file_name = ""
        self.title("Chess notes")
        self.geometry("1250x655")
        self.update_idletasks()
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

        self.pgn_text = Text(self.moves_frame)
        self.pgn_text.pack(side = TOP)

        self.save_button = Button(self.moves_frame, text = "Save", width = 45, command = self.save_chess_tree)
        self.save_button.pack(side = LEFT)
        #self.save_button.bind("<Button-1>", self.save_chess_tree)

        self.load_button = Button(self.moves_frame, text = "Load", width = 45, command = self.load_chess_tree)
        self.load_button.pack(side = RIGHT)

        self.board_frame = Frame(self)
        self.board_frame.pack(side = RIGHT)

        self.canvas = Canvas(self.board_frame, width = self.winfo_width() // 2, height = 605)
        #self.canvas.bind('<Button-1>', self.canvas_clicked)
        self.canvas.bind('<Button-1>', self.canvas_tapped)
        #self.canvas.bind('<ButtonRelease>', self.canvas_released)
        self.canvas.bind('<ButtonRelease>', self.canvas_untapped)
        self.canvas.pack()

        self.board_img = ImageTk.PhotoImage(Image.open("../assets/board_image_1.png"))
        self.canvas.create_image(300, 305, anchor = "center", image = self.board_img)

        self.full_back_image = ImageTk.PhotoImage(Image.open("../assets/full_back.png"))
        self.full_back_button = Button(self.board_frame, width = 150, height= 50, image = self.full_back_image)
        self.full_back_button.pack(side = LEFT)

        self.back_image = ImageTk.PhotoImage(Image.open("../assets/back.png"))
        self.back_button = Button(self.board_frame, width = 150, height= 50, image = self.back_image)
        self.back_button.pack(side = LEFT)

        self.move_image = ImageTk.PhotoImage(Image.open("../assets/move.png"))
        self.move_button = Button(self.board_frame, width = 150, height= 50, image = self.move_image)
        self.move_button.pack(side = LEFT)

        self.full_move_image = ImageTk.PhotoImage(Image.open("../assets/full_move.png"))
        self.full_move_button = Button(self.board_frame, width = 150, height= 50, image = self.full_move_image)
        self.full_move_button.pack(side = LEFT)

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

    def move_piece_img(self, start_rank, start_line, end_rank, end_line):

        #start_rank = self.start_rank
        #start_line = self.start_line
        #end_rank = self.end_rank
        #end_line = self.end_line

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
            #self.board.board[rank][line].piece_img = None
            self.clear_canvas_square(self.board.board[rank][line])
            return

        if len(comment) == 4:
            start_rank = int(comment[0])
            start_line = int(comment[1])
            end_rank = int(comment[2])
            end_line = int(comment[3])
            self.move_piece_img(start_rank, start_line, end_rank, end_line)


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
            self.board, comment = Move.Move.do_move(start_square, end_square, self.board)
            print(comment)

            self.move_piece_img(self.start_rank, self.start_line, self.end_rank, self.end_line)
            self.process_comment_from_move(comment)
        else:
            print("Ilegal")
            self.start_line = self.end_line = self.start_rank = self.end_rank = -1

        #self.board.castles.print_castles()
        #self.board.print_position_as_text_from_white()


    def actualize(self):
        pass

    """
    def canvas_clicked(self, event):
        if not (self.top_pad < event.y < self.bottom_pad) or not (self.left_pad < event.x < self.right_pad):
            return

        x_center, y_center = self.get_square_center(event.x, event.y)
        line, rank = self.get_square_axises(x_center, y_center)
        considered_square = self.board.board[line][rank]
        if not considered_square.piece_stands():
            return

        self.last_cursor_x = event.x
        self.last_cursor_y = event.y
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
    def canvas_released(self, event):
        print("HELLO")
        if self.last_cursor_x == -1:
            return

        if not (self.top_pad < event.y < self.bottom_pad) or not (self.left_pad < event.x < self.right_pad):
            self.last_cursor_y = -1
            self.last_cursor_x = -1
            return

        x_center, y_center = self.get_square_center(event.x, event.y)
        line, rank = self.get_square_axises(x_center, y_center)
        considered_square = self.board.board[line][rank]

        last_x_center, last_y_center = self.get_square_center(self.last_cursor_x, self.last_cursor_y)
        last_line, last_rank = self.get_square_axises(last_x_center, last_y_center)
        considered_last_square = self.board.board[last_line][last_rank]
        print("HELLO")
        print(last_line, last_rank)
        considered_last_square.print_square()
        considered_square.print_square()

        if not Move.Move.check_move_legal(start_square=considered_last_square, end_square=considered_square, board=self.board):
            self.last_cursor_x = -1
            self.last_cursor_y = -1
            return

        id = self.canvas.create_image(x_center, y_center, anchor="center", image=considered_last_square.piece_img)
        #update square info
        if considered_square.piece_stands():
            self.canvas.delete(considered_square.canvas_id)
        #considered_square.set_piece(considered_last_square.piece)
        Move.Move.do_move(considered_last_square, considered_square, self.board)
        #self.draw_pieces()
        #self.actualize_board_look()
        self.board.print_position_as_text_from_white()
        # actualize board look after move done
        # make proper castle
        considered_square.piece_img = considered_last_square.piece_img
        considered_square.canvas_id = id
        #clear old
        self.clear_canvas_square(considered_last_square)
    """

    def open_setup_window(self):
        setup_window = BoardSetup.board_set(self)
        self.wait_window(setup_window)

    def calc_square_size(self):
        return (self.bottom_pad - self.top_pad) / 8

    def get_square_center_by_line_rank(self, line, rank):
        half_square = (self.bottom_pad - self.top_pad) / 16
        sqaure_side = self.calc_square_size()
        if not self.board_reverted:
            x_center = self.left_pad + half_square + sqaure_side * line
            y_center = self.top_pad + half_square + sqaure_side * (7 - rank)

        return x_center, y_center

    def clear_canvas_square(self, square: Square.Square):
        self.canvas.delete(square.canvas_id)
        square.canvas_id = 0
        square.piece_img = None


    def draw_piece_on_square(self, square: Square):
        #self.clear_canvas_square(square)
        #self.canvas.delete(square.canvas_id)
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

    def create_new_setup(self, event):
        self.open_setup_window()
        self.draw_pieces()
        return "break"
        #bind applying to apply button

    def chess_tree_to_file(self, some_obj):
        return some_obj

    def file_to_chess_tree(self, some_obj):
        return some_obj

    def save_chess_tree(self):
        path = filedialog.asksaveasfilename(initialfile= "Untitled", defaultextension='.txt', filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if path:
            text_to_save = self.chess_tree_to_file(self.pgn_text.get(1.0, END))
            lines = text_to_save.split('\n')
            with open(path, 'w+') as f:
                for line in lines:
                    f.write(line + '\n')


    def load_chess_tree(self):
        path = filedialog.askopenfile(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if path:
            print(path.name)
            with open(path.name, 'r') as f:
                lines = path.readlines()
                print(lines)
        else:
            print("No file")
        #self.load_button.update()

    def full_back(self):
        pass

    def set_canvas_board(self, board: Board.Board) -> None:
        self.board = board

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

    def draw_empty_board(self):
        self.canvas.pack()
        img = ImageTk.PhotoImage(Image.open("../assets/board_image_1.png"))
        b = self.canvas.create_image(300, 305, anchor = "center", image = img)
        self.mainloop()

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

