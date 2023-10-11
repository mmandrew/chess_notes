import os
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
import Board
import Square
import Consts
import BoardSetup

class chessCanvas(tk.Tk):
    def __init__(self): #, window: Tk):
        board_image = []
        super().__init__()
        self.current_file_name = ""
        self.title("Chess notes")
        self.geometry("1250x655")
        self.update_idletasks()
        self.board = Board.Board()

        self.moves_frame = Frame(self, width=600)
        self.moves_frame.pack(side = LEFT)

        self.new_button = Button(self.moves_frame, text = "New", width = 91)
        self.new_button.update_idletasks() ##???
        self.new_button.pack(side = TOP)
        self.new_button.bind("<Button-1>", self.open_setup_window)

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

    def open_setup_window(self, event):
        setup_window = BoardSetup.board_set(self)
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

