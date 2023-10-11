import os
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
import Board
import Square
import Consts
import chessCanvas
import SetBoardFrame

class board_set(tk.Toplevel):
    def __init__(self, window):
        super().__init__(window)
        self.title("Set custom position")
        self.geometry("1500x900")
        self.grab_set()

        self.basic_frame = Frame(self, width = 400, height = 900)
        self.basic_frame.pack(side = LEFT, fill='both')

        self.clear_board_button = Button(self.basic_frame, text = "Clear board", width = 50)
        self.clear_board_button.bind('<Button-1>', self.clear_board)
        self.clear_board_button.pack(side = TOP, pady = 100)
        self.start_position_button = Button(self.basic_frame, text = "Set start position", width = 50)
        self.start_position_button.bind('<Button-1>', self.set_start_position)
        self.start_position_button.pack(side = TOP, pady = 100)
        self.flip_board_buttom = Button(self.basic_frame, text = "Flip board", width = 50)
        self.flip_board_buttom.pack(side = TOP, pady = 100)
        self.apply_button = Button(self.basic_frame, text = "APPLY", width = 50)
        self.apply_button.pack()

        #self.board_and_pieces_frame = Frame(self, width = 700, height = 900, bg = "white")
        self.board_and_pieces_frame = SetBoardFrame.set_board_frame(self)
        self.board_and_pieces_frame.pack(side=LEFT)

        self.position_details_frame = Frame(self, width = 400, height = 700)
        self.position_details_frame.pack(side = LEFT, fill = 'both')

        self.white_label = Label(self.position_details_frame, text = "White")
        self.white_label.grid(row = 0, column = 0, sticky=N)

        self.white_king_castle_check_state = BooleanVar()
        self.white_king_castle_check = Checkbutton(self.position_details_frame, text = "O-O", onvalue = True, offvalue= False, variable = self.white_king_castle_check_state)
        self.white_king_castle_check.grid(row = 1, column = 0, sticky=W)

        self.white_queen_castle_check_state = BooleanVar()
        self.white_queen_castle_check = Checkbutton(self.position_details_frame, text = "O-O-O", onvalue = True, offvalue= False, variable = self.white_queen_castle_check_state)
        self.white_queen_castle_check.grid(row = 2, column = 0, sticky=W)

        self.black_label = Label(self.position_details_frame, text = "Black")
        self.black_label.grid(row = 0, column = 1, sticky=N)

        self.black_king_castle_check_state = BooleanVar()
        self.black_king_castle_check = Checkbutton(self.position_details_frame, text = "O-O", onvalue = True, offvalue= False, variable = self.black_king_castle_check_state)
        self.black_king_castle_check.grid(row = 1, column = 1, sticky=W)

        self.black_queen_castle_check_state = BooleanVar()
        self.black_queen_castle_check = Checkbutton(self.position_details_frame, text = "O-O-O", onvalue = True, offvalue= False, variable = self.black_queen_castle_check_state)
        self.black_queen_castle_check.grid(row = 2, column = 1, sticky=W)

        self.ep_label = Label(self.position_details_frame, text = "e.p. square")
        self.ep_label.grid(row = 3, column = 0, pady=100)

        self.ep_text = Text(self.position_details_frame, width = 15, height = 1)
        self.ep_text.grid(row = 3, column = 1, rowspan = 1, columnspan = 1)
        self.ep_text.config(state = DISABLED)

        self.move_order = StringVar(value="White")
        self.move_label = Label(self.position_details_frame, text = "Move")
        self.move_label.grid(row = 4, column = 0)

        self.white_move_button = Radiobutton(self.position_details_frame, text = "White", value = "White", variable = self.move_order)
        self.white_move_button.grid(row = 5, column = 0)
        self.black_move_buttom = Radiobutton(self.position_details_frame, text = "Black", value = "Black", variable = self.move_order)
        self.black_move_buttom.grid(row = 6, column = 0)

    def clear_board(self, event):
        self.board_and_pieces_frame.clear_canvas_board()

    def set_start_position(self, event):
        self.board_and_pieces_frame.clear_canvas_board()
        self.board_and_pieces_frame.board.set_start_position()
        self.board_and_pieces_frame.draw_board()
        self.white_move_button.select()
        self.ep_text.delete(1.0, END)
        self.white_king_castle_check.select()
        self.white_queen_castle_check.select()
        self.black_king_castle_check.select()
        self.black_queen_castle_check.select()

    def reverse_board(self, event):
        pass

    def apply(self, event):
        pass

    def set_current_piece(self, event):
        pass



if __name__ == "__main__":
    pass