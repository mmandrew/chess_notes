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
    def __init__(self, toplevel_window, board):
        super().__init__(toplevel_window, width = 700, height = 900)
        self.top = toplevel_window
        self.board = board.copy_self()
        self.white_pieces_images = []
        self.white_pieces_btns = []
        self.black_pieces_images = []
        self.black_pieces_btns = []
        self.board_reverted = False
        self.boarded_pieces = []

        self.moving_image = None
        self.moving_id = None
        self.last_cursor_x = -1
        self.last_cursor_y = -1

        self.test_id = 0
        self.test_img = None

        self.left_pad = 20
        self.right_pad = 593
        self.bottom_pad = 583
        self.top_pad =  10

        self.canvas = Canvas(self, width = 600, height = 605, bg = "white")
        self.canvas.grid(row = 0, column = 0, rowspan = 7, columnspan = 7)
        self.canvas.bind('<Button-1>', self.board_pressed)
        self.canvas.bind('<Button-3>', self.set_square_ep)
        self.canvas.bind('<ButtonRelease>', self.released)

        self.board_img = ImageTk.PhotoImage(Image.open("../assets/board_image_1.png"))
        self.board_id = self.canvas.create_image(300, 305, anchor = 'center', image = self.board_img)

        for i, piece in enumerate(Consts.piece_shorts):
            piece_img = ImageTk.PhotoImage(Image.open("../assets/{}_{}.png".format(piece, 'w')))
            self.white_pieces_images.append(piece_img)
            btn = Button(self, image = piece_img, command=lambda j = i, color = self.white_pieces_btns: self.piece_button(j, color))
            self.white_pieces_btns.append(btn)
            btn.grid(row = 7, column = i)

            piece_img = ImageTk.PhotoImage(Image.open("../assets/{}_{}.png".format(piece, 'b')))
            self.black_pieces_images.append(piece_img)
            btn = Button(self, image = piece_img, command=lambda j = i, color = self.black_pieces_btns: self.piece_button(j, color))
            self.black_pieces_btns.append(btn)
            btn.grid(row = 8, column = i)

        self.cursor_image = ImageTk.PhotoImage(Image.open("../assets/cursor_2.png"))
        self.cursor_button = Button(self, image = self.cursor_image, command = lambda j = -1, color = "cursor": self.piece_button(j, color))
        self.cursor_button.config(background="green")
        self.active_piece_button = self.cursor_button
        self.cursor_button.grid(row = 7, column = 6)

        self.trash_image = ImageTk.PhotoImage(Image.open("../assets/trash.png"))
        self.trash_button = Button(self, image = self.trash_image, command = lambda j = -1, color = "trash": self.piece_button(j, color))
        self.trash_button.grid(row = 8, column = 6)

        self.draw_board()

    def change_board_image(self, img_path):
        self.canvas.delete(self.board_id)
        self.board_img = ImageTk.PhotoImage(Image.open(img_path))
        self.board_id = self.canvas.create_image(300, 305, anchor = 'center', image = self.board_img)

    def piece_button(self, j, color):
        if (j == -1) and color == "cursor":
            self.active_piece_button.config(background="SystemButtonFace")
            self.active_piece_button = self.cursor_button
            self.cursor_button.config(background="green")
            return

        if (j == -1) and color == "trash":
            self.active_piece_button.config(background="SystemButtonFace")
            self.active_piece_button = self.trash_button
            self.trash_button.config(background="green")
            return

        self.active_piece_button.config(background="SystemButtonFace")
        self.active_piece_button = color[j]
        color[j].config(background="green")

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
        else:
            x_center = self.left_pad + half_square + sqaure_side * (7 - line)   #?
            y_center = self.top_pad + half_square + sqaure_side  * rank               #?

        return x_center, y_center

    def calc_square_size(self):
        return (self.bottom_pad - self.top_pad) / 8

    def get_square_axises(self, x, y):
        square_size = self.calc_square_size()
        x_axis = math.floor((x - self.left_pad) / square_size)
        y_axis = math.floor((y - self.top_pad) / square_size)
        if not self.board_reverted:
            return 7 - y_axis, x_axis #line, rank
        else:
            return y_axis, 7 - x_axis  #?

    def get_piece_by_current_active_piece(self):
        if self.active_piece_button in self.white_pieces_btns:
            color = 'w'
            piece = Consts.piece_set[self.white_pieces_btns.index(self.active_piece_button)]

        if self.active_piece_button in self.black_pieces_btns:
            color = 'b'
            piece = Consts.piece_set[self.black_pieces_btns.index(self.active_piece_button)]

        return piece, color

    def set_square_ep(self, event):
        ep_value = self.top.ep_text.get(1.0, END)
        x_center, y_center = self.get_square_center(event.x, event.y)
        line, rank = self.get_square_axises(x_center, y_center)
        considered_square = self.board.board[line][rank]

        self.top.ep_text.config(state = NORMAL)
        self.top.ep_text.delete(1.0, END)
        if not ((ep_value[0] == considered_square.line) and (ep_value[1] == str(considered_square.rank))):
            self.top.ep_text.insert(1.0, "{}{}".format(considered_square.line, considered_square.rank))
        self.top.ep_text.config(state = DISABLED)


    def board_pressed(self, event):
        if not (self.top_pad < event.y < self.bottom_pad) or not (self.left_pad < event.x < self.right_pad):
            return

        x_center, y_center = self.get_square_center(event.x, event.y)
        line, rank = self.get_square_axises(x_center, y_center)
        considered_square = self.board.board[line][rank]

        if self.active_piece_button in self.white_pieces_btns:
            target_images = self.white_pieces_images
            target_btns = self.white_pieces_btns

        if self.active_piece_button in self.black_pieces_btns:
            target_images = self.black_pieces_images
            target_btns = self.black_pieces_btns

        if (self.active_piece_button in self.white_pieces_btns) or (self.active_piece_button in self.black_pieces_btns):
            image_to_put = target_images[target_btns.index(self.active_piece_button)]
            considered_square.piece_img = image_to_put

            if  considered_square.canvas_id == 0:
                considered_square.canvas_id = self.canvas.create_image(x_center, y_center, anchor="center",
                                                        image=image_to_put)
                considered_square.set_piece(Piece.Piece(*self.get_piece_by_current_active_piece()))
            else:
                if (considered_square.piece.name, considered_square.piece.color) == self.get_piece_by_current_active_piece():
                    self.canvas.delete(considered_square.canvas_id)
                    considered_square.clear()
                    considered_square.canvas_id = 0
                    considered_square.piece_img = None
                else:
                    self.canvas.delete(considered_square.canvas_id)
                    considered_square.canvas_id = self.canvas.create_image(x_center, y_center, anchor="center",
                                                                           image=image_to_put)
                    considered_square.set_piece(Piece.Piece(*self.get_piece_by_current_active_piece()))
                    considered_square.piece_img = image_to_put

        if self.active_piece_button == self.trash_button:
            if considered_square.piece_stands():
                self.canvas.delete(considered_square.canvas_id)
                considered_square.canvas_id = 0
                considered_square.clear()

        if self.active_piece_button == self.cursor_button:
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

        if not self.active_piece_button == self.cursor_button:
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

    def reverse_all_piece_images(self):
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
        print("RANK", square.rank)
        rank = square.rank - 1
        x_center, y_center = self.get_square_center_by_line_rank(line, rank)

        #create new on new axises
        square.canvas_id = self.canvas.create_image(x_center, y_center, anchor = 'center', image = piece_img)
        square.piece_img = piece_img


if __name__ == "__main__":
    pass
