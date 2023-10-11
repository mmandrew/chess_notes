import os
import time
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
import Board
import Square
import Consts
import chessCanvas
import math
import Piece

class set_board_frame(tk.Frame):
    def __init__(self, main_frame):
        super().__init__(main_frame, width = 700, height = 900)
        self.top = main_frame
        self.board = Board.Board()
        self.white_pieces_images = []
        self.black_pieces_images = []
        self.board_reverted = False
        self.boarded_pieces = []

        self.moving_image = None
        self.moving_id = None
        self.last_cursor_x = -1
        self.last_cursor_y = -1

        self.left_pad = 20
        self.right_pad = 593
        self.bottom_pad = 583
        self.top_pad = 10

        self.canvas = Canvas(self, width = 600, height = 605, bg = "white")
        self.canvas.bind('<Button-1>', self.board_pressed)
        self.canvas.bind('<ButtonRelease>', self.released)

        self.board_img = ImageTk.PhotoImage(Image.open("../assets/board_image_1.png"))
        self.canvas.create_image(300, 305, anchor = 'center', image = self.board_img)

        for i, piece in enumerate(Consts.piece_shorts):
            piece_img = ImageTk.PhotoImage(Image.open("../assets/{}_{}.png".format(piece, 'w')))
            self.white_pieces_images.append(piece_img)

            piece_img = ImageTk.PhotoImage(Image.open("../assets/{}_{}.png".format(piece, 'b')))
            self.black_pieces_images.append(piece_img)

        self.cursor_image = ImageTk.PhotoImage(Image.open("../assets/cursor_2.png"))

    def get_square_center(self, x, y):
        half_square = (self.bottom_pad - self.top_pad) / 16
        sqaure_side = self.calc_square_size()
        x_center = self.left_pad + half_square + sqaure_side * int((x - self.left_pad) / sqaure_side)
        y_center = self.top_pad +half_square + sqaure_side * int((y - self.top_pad) / sqaure_side)
        return x_center, y_center

    def get_square_center_by_line_rank(self, line, rank):
        half_square = (self.bottom_pad - self.top_pad) / 16
        sqaure_side = self.calc_square_size()
        if not self.board_reverted:
            x_center = self.left_pad + half_square + sqaure_side * line
            y_center = self.top_pad + half_square + sqaure_side * (7 - rank)

        return x_center, y_center

    def calc_square_size(self):
        return (self.bottom_pad - self.top_pad) / 8

    def get_square_axises(self, x, y):
        square_size = self.calc_square_size()
        x_axis = math.floor((x - self.left_pad) / square_size)
        y_axis = math.floor((y - self.top_pad) / square_size)
        if not self.board_reverted:
            return 7 - y_axis, x_axis #line, rank

    def board_pressed(self, event):
        if not (self.top_pad < event.y < self.bottom_pad) or not (self.left_pad < event.x < self.right_pad):
            return

        x_center, y_center = self.get_square_center(event.x, event.y)
        line, rank = self.get_square_axises(x_center, y_center)
        considered_square = self.board.board[line][rank]

        if considered_square.piece_stands():
            self.moving_image = considered_square.piece_img
            self.moving_id = considered_square.canvas_id
            self.last_cursor_x = event.x
            self.last_cursor_y = event.y
        else:
            self.moving_id = None
            self.moving_image = None

    def clear_canvas_square(self, square: Square.Square):
        self.canvas.delete(square.canvas_id)
        square.clear()
        square.canvas_id = 0
        square.piece_img = None

    def released(self, event):
        if not (self.top_pad < event.y < self.bottom_pad) or not (self.left_pad < event.x < self.right_pad):
            last_x_center, last_y_center = self.get_square_center(self.last_cursor_x, self.last_cursor_y)
            last_line, last_rank = self.get_square_axises(last_x_center, last_y_center)
            considered_last_square = self.board.board[last_line][last_rank]
            self.clear_canvas_square(considered_last_square)
            return

        x_center, y_center = self.get_square_center(event.x, event.y)
        line, rank = self.get_square_axises(x_center, y_center)
        considered_square = self.board.board[line][rank]
        last_x_center, last_y_center = self.get_square_center(self.last_cursor_x, self.last_cursor_y)
        last_line, last_rank = self.get_square_axises(last_x_center, last_y_center)
        considered_last_square = self.board.board[last_line][last_rank]
        if self.moving_image:
            self.moving_id = self.canvas.create_image(x_center, y_center, anchor="center",
                                                                               image=self.moving_image)
            #update square info
            if considered_square.piece_stands():
                self.canvas.delete(considered_square.canvas_id)
            considered_square.set_piece(considered_last_square.piece)
            considered_square.piece_img = self.moving_image
            considered_square.canvas_id = self.moving_id
            #clear old
            #self.canvas.delete(considered_last_square.canvas_id)
            #considered_last_square.clear()
            self.clear_canvas_square(considered_last_square)

    def clear_canvas_board(self):
        for rank in self.board.board:
            for square in rank:
                self.clear_canvas_square(square)

    def draw_piece_on_square(self, square: Square.Square):
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

    def draw_board(self):
        for rank in self.board.board:
            for square in rank:
                self.draw_piece_on_square(square)







if __name__ == "__main__":
    pass
