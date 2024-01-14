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
    def __init__(self, window, board: Board):
        super().__init__(window)
        self.window = window
        self.board = board.copy_self()
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
        self.flip_board_button = Button(self.basic_frame, text = "Flip board", width = 50)
        self.flip_board_button.bind('<Button-1>', self.flip_canvas)
        self.flip_board_button.pack(side = TOP, pady = 100)
        self.apply_button = Button(self.basic_frame, text = "APPLY", width = 50)
        self.apply_button.bind('<Button-1>', self.apply)
        self.apply_button.pack()

        #self.board_and_pieces_frame = Frame(self, width = 700, height = 900, bg = "white")
        self.board_and_pieces_frame = SetBoardFrame.set_board_frame(self, board)
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

        self.board_reverted = False

        self.white_move_button = Radiobutton(self.position_details_frame, text = "White", value = "w", variable = self.move_order)
        self.white_move_button.grid(row = 5, column = 0)
        self.white_move_button.select()
        self.black_move_buttom = Radiobutton(self.position_details_frame, text = "Black", value = "b", variable = self.move_order)
        self.black_move_buttom.grid(row = 6, column = 0)
        self.bring_castles()
        self.bring_ep_square()
        self.bring_move_order()

    def flip_canvas(self, event):
        self.flip_board()
        self.flip_pieces()

    def flip_board(self):
        if not self.board_reverted:
            self.board_and_pieces_frame.change_board_image("../assets/board_revert.png")
            self.board_and_pieces_frame.board_reverted = True
            self.board_reverted = True
        else:
            self.board_and_pieces_frame.change_board_image("../assets/board_image_1.png")
            self.board_and_pieces_frame.board_reverted = False
            self.board_reverted = False

    def flip_pieces(self):
        self.board_and_pieces_frame.reverse_all_piece_images()

    def bring_castles(self):
        if self.board.castles.white_kingside_castle_possible:
            self.white_king_castle_check.select()
        if self.board.castles.black_kingside_castle_possible:
            self.black_king_castle_check.select()
        if self.board.castles.white_queenside_castle_possible:
            self.white_queen_castle_check.select()
        if self.board.castles.black_queenside_castle_possible:
            self.black_queen_castle_check.select()

    def bring_ep_square(self):
        self.ep_text.config(state=NORMAL)
        self.ep_text.insert(1.0, "{}".format(self.board.ep_square))
        self.ep_text.config(state=DISABLED)

    def bring_move_order(self):
        if self.board.move_order == 'w':
            self.white_move_button.select()
        else:
            self.black_move_buttom.select()

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
        self.window.board.castles.print_castles()
        self.window.full_board_clear()
        self.window.board = self.board_and_pieces_frame.board
        self.window.clear_pgn()

        if self.white_king_castle_check_state.get():
            self.window.board.castles.set_white_kingside_castle_possible()
        else:
            self.window.board.castles.set_white_kingside_castle_impossible()

        if self.black_king_castle_check_state.get():
            self.window.board.castles.set_black_kingside_castle_possible()
        else:
            self.window.board.castles.set_black_kingside_castle_impossible()

        if self.white_queen_castle_check_state.get():
            self.window.board.castles.set_white_queenside_castle_possible()
        else:
            self.window.board.castles.set_white_queenside_castle_impossible()

        if self.black_queen_castle_check_state.get():
            self.window.board.castles.set_black_queenside_castle_possible()
        else:
            self.window.board.castles.set_black_queenside_castle_impossible()

        ep = self.ep_text.get("1.0", END)[:-1] or ''
        self.window.board.ep_square = self.ep_text.get("1.0", END)[:-1] or ''
        if ep:
            self.window.board.set_ep_square(ep)
        self.window.board.move_order = self.move_order.get()
        self.window.board.castles.print_castles()

        self.destroy()
        pass

    def set_current_piece(self, event):
        pass


if __name__ == "__main__":
    pass