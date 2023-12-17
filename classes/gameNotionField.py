import os
import tkinter.ttk
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import tkinter as tk
from PIL import ImageTk, Image
import Board
import Square
import Consts
import chessCanvas
import SetBoardFrame
import Fen

class gameNotionField(scrolledtext.ScrolledText):
    def __init__(self, start_board: Board.Board(), *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tab_len = 4

        self.start_board: Board.Board() = start_board.copy_self()

        #self.current_move = [0, 1, 'w'] #(line, move, order). line and move start from 1 !!!
        self.current_move = {"line": 0, "move": 1, "order": 'w'}
        self.lines = ["START"]
        self.lines_and_fens = [[{"move": "START", "fen": self.start_board.board_to_fen()}], []]

        self.bind("<Button-3>", self.test_record_a_move)
        #self.bind("<Button-1>", self.go_to_move)
        self.bind("<Key>", self.remember_text)
        self.bind("<<Modified>>", self.remember_text)

    def tab_counter_in_line(self, index):
        space_counter = 0
        while self.lines[space_counter] != ' ':
            space_counter += 1

        return space_counter/self.tab_len


    def set_start_board(self, start_board: Board.Board):
        self.start_board = start_board.copy_self()
        self.lines_and_fens[0][0]["fen"] = self.start_board.board_to_fen()

    def update_moves_lines(self):
        text = self.get(1.0, END)
        self.lines = ["START"] + text.split("\n")[:-1]

    def update_moves_and_fens(self):
        pass

    def flip_move_order(self):
        if self.current_move["order"] == 'w':
            self.current_move["order"] = 'b'
        else:
            self.current_move["order"] = "w"

    def get_cursor_pos(self):
        for line in self.lines:
            print("line", line)
        moves = ' '.join(lines[self.current_move["line"]].split(' ')[:self.current_move["move"]])
        return len(moves) + 1

    def remember_text(self, event):
        self.update_moves_lines()

    def base_record_move(self, move_note, fen_after_move):
        current_move_number = self.current_move["move"]
        move_line = self.current_move["line"]
        if self.current_move["order"] == 'b':
            move_rec = ' {}'.format(move_note)
            self.insert(END, ' {}'.format(move_note))
            self.current_move["move"] += 1

            if not move_line < len(self.lines_and_fens):
               self.lines_and_fens.append([])
            self.lines_and_fens[move_line].append({"move": move_rec, "fen": fen_after_move})

            self.current_move["line"] += 1
        else:
            self.current_move["line"] += 1
            move_line = self.current_move["line"]
            move_rec = '{}){}'.format(current_move_number, move_note)
            if move_line == 1:
                self.insert(END, move_rec)
            else:
                self.insert(END, '\n' + move_rec)

            if not move_line < len(self.lines_and_fens):
               self.lines_and_fens.append([])
            self.lines_and_fens[move_line].append({"move": move_rec, "fen": fen_after_move})

        return move_line

    def side_record_move(self, move_note, fen_after_move):
        print("SIDE RECORD HERE")
        pass

    def test_record_a_move(self, event):
        self.base_record_move()
        self.flip_move_order()

    def reposition_current_move(self, line_num: int, left_space: int, right_space: int) -> None:
        self.current_move["line"] = line_num
        line = self.lines[self.current_move["line"]]

        move_rec = line[left_space + 1:right_space]
        if ')' in move_rec:
            if "..." in move_rec:
                self.current_move["order"] = 'w'
                self.current_move["move"] = int(move_rec[:move_rec.find(')')]) + 1
            else:
                self.current_move["order"] = 'b'
                self.current_move["move"] = int(move_rec[:move_rec.find(')')])
        else:
            self.current_move["order"] = 'w'
            index = left_space - 1
            while (line[index] != ' ') and index > 0:
                index -= 1
            if index > 0:
                prev_move_rec = line[index + 1:left_space]
            else:
                prev_move_rec = line[index:left_space]
            self.current_move["move"] = int(prev_move_rec[:prev_move_rec.find(')')]) + 1
        print("END OF REPOSITION", self.current_move)

    def highlight_move(self, line_num: int, char_num: int) -> None:

        if char_num >= len(self.lines[line_num]):
            char_num = len(self.lines[line_num]) - 1

        current_line = self.lines[line_num]
        if len(current_line) == 0:
            return

        if current_line[char_num] == ' ':
            left_space = char_num - 1
        else:
            left_space = char_num

        while current_line[left_space] != ' ':
            left_space -= 1
            if left_space == -1:
                break

        right_space = char_num
        while current_line[right_space] != ' ':
            right_space += 1
            if right_space == len(current_line):
                break

        self.tag_delete("black")
        self.tag_config("black", background="black", foreground="white")
        self.tag_add("black", "{}.{}".format(line_num, left_space + 1), "{}.{}".format(line_num, right_space))
        self.reposition_current_move(line_num, left_space, right_space)
        return left_space

    def get_fen_after_move(self, line_num, left_space_index):
        left_part = self.lines[line_num][:left_space_index + 1]
        space_count = left_part.count(" ")

        return self.lines_and_fens[line_num][space_count]["fen"]

    def go_to_move(self, event):
        self.update_moves_lines()
        line_num, char_num = [int(index) for index in self.index("current").split('.')]
        left_space_index = self.highlight_move(line_num, char_num)
        fen_to_set = Fen.Fen(self.get_fen_after_move(line_num, left_space_index))
        boart_to_set = fen_to_set.fen_to_board()
        return boart_to_set
        #fen_to_set.fen_to_board().print_position_as_text_from_white()


    def record_a_move(self, move_note, fen_after_move):
        if ((self.current_move["order"] == 'w') and (len(self.lines) == self.current_move["line"] + 1)) or \
            ((self.current_move["order"] == 'b') and (len(self.lines) - 1 == self.current_move["line"])):
            move_line = self.base_record_move(move_note, fen_after_move)
        else:
            move_line = self.side_record_move(move_note, fen_after_move)
        print("MOVE_LINE", move_line)
        self.update_moves_lines()
        move_index = len(self.lines[move_line]) - 1
        self.highlight_move(move_line, move_index)

    def next_move(self):
        pass

    def prev_move(self):
        pass

    def set_pos_by_move(self):
        pass

    def full_back(self):
        pass

    def full_forward(self):
        pass

    def restore_position_by_current_move(self):
        pass



if __name__ == "__main__":
    pass
