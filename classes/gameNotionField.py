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
    def __init__(self, start_board: Board.Board, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tab_len = 4

        self.start_board: Board.Board() = start_board.copy_self()

        #self.current_move = [0, 1, 'w'] #(line, move, order). line and move start from 1 !!!
        print(start_board.move_order)
        print(self.start_board.move_order)
        self.clear()

        self.bind("<Button-3>", self.test_record_a_move)
        #self.bind("<Button-1>", self.go_to_move)
        self.bind("<Key>", self.remember_text)
        self.bind("<<Modified>>", self.remember_text)

    def clear(self):
        self.delete(1.0, END)
        self.current_move = {"line": int(self.start_board.move_order == 'b'), "move": 1, "order": self.start_board.move_order}
        self.lines = ["START"]
        self.lines_and_fens = [[{"move": "START", "fen": self.start_board.board_to_fen()}], []]

    def space_counter_in_line(self, index):
        space_counter = 0
        while self.lines[index][space_counter] == ' ':
            space_counter += 1

        return space_counter

    def set_start_board(self, start_board: Board.Board):
        self.start_board = start_board.copy_self()
        self.lines_and_fens[0][0]["fen"] = self.start_board.board_to_fen()
        self.current_move["order"] = self.start_board.move_order
        if self.current_move["order"] == "b":
            print("BLACK TO MOVE")
            self.current_move["line"] = 1
            self.insert(1.0, "1)...")
            self.lines.append("1)...")
        else:
            print("WHITE TO MOVE")

    def update_moves_lines(self):
        text = self.get(1.0, END)
        self.lines = ["START"] + text.split("\n")[:-1]

    def update_text_by_lines(self):
        self.delete(1.0, END)
        self.insert(1.0, self.lines[1])
        for line in self.lines[2:]:
            self.insert(END, "\n" + line)

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
        print("LINES NOW")
        print(self.lines)
        s = self.get_right_space_by_current_move()
        #print(s, s[-1])
        right_space = len(s)

        current_line = self.lines[self.current_move["line"]]
        print("RIGHT SPACE", right_space)
        print("CURRENT LINE", len(current_line), current_line)
        if ((right_space < len(current_line)) or (current_line[0] != ' ')):
            print("CARRIYNG")
            r = self.compose_inter_string_carriyng(move_note, right_space)
            self.add_fen_for_side_move_carriyng(move_note, fen_after_move, right_space)
        else:
            print("NOT CARRIYNG")
            r = self.compose_inter_string_not_carriyng(move_note, right_space)
            self.add_fen_for_side_move_not_carriyng(move_note, fen_after_move)

        return r

    def test_record_a_move(self, event):
        self.base_record_move()
        self.flip_move_order()

    def span_spaces_at_start(self, s):
        if not s:
            return ''
        s1 = s
        while s1[0] == ' ':
            s1 = s1[1:]
            if not s1:
                return ''
        return s1

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
            print("PREMOVE SHIT ", line, index, left_space, prev_move_rec, prev_move_rec[:prev_move_rec.find(')')])
            self.current_move["move"] = int(prev_move_rec[:prev_move_rec.find(')')]) + 1

    def get_left_and_right_space_around_char_num(self, line_num, char_num):
        current_line = self.lines[line_num]
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

        return [left_space, right_space]

    def get_right_space_by_current_move(self): #basically it is a right space of highlighted move
        current_line = self.lines[self.current_move["line"]]
        print("CURRENT LINE ", current_line)
        if self.current_move["order"] == "b":
            current_move = self.current_move["move"]
        else:
            current_move = self.current_move["move"] - 1
        pre_move_num_part, after_move_num_part = current_line.split(str(current_move) + ')')
        after_move_num_part = str(current_move) + ')' + after_move_num_part
        if self.current_move["order"] == "b":
            return pre_move_num_part + after_move_num_part.split(' ')[0]
        else:
            return pre_move_num_part + ' '.join(after_move_num_part.split(' ')[:2])

    def add_fen_for_side_move_carriyng(self, move_rec, pos_fen, right_space):
        current_line_num = self.current_move["line"]
        space_count = self.span_spaces_at_start(self.lines[current_line_num][:right_space]).count(' ')
        after_move = self.lines_and_fens[current_line_num][space_count + 1:]
        self.lines_and_fens[current_line_num] = self.lines_and_fens[current_line_num][:space_count + 1]

        self.lines_and_fens.insert(current_line_num + 1, [])
        if (self.current_move["order"] == "b") and (len(after_move) > 0):
            self.lines_and_fens.insert(current_line_num + 2, after_move)

        self.lines_and_fens[current_line_num + 1].append({"move": move_rec, "fen": pos_fen})

        if (self.current_move["order"] == "w") and len(after_move) > 0:
            self.lines_and_fens.insert(current_line_num + 2, after_move)

    def add_fen_for_side_move_not_carriyng(self, move_rec, pos_fen):
        current_line_num = self.current_move["line"]
        self.lines_and_fens[current_line_num].append({"move": move_rec, "fen": pos_fen})

    def compose_inter_string_carriyng(self, move_rec, right_space):
        inter_string = ""
        current_line = self.lines[self.current_move["line"]]

        if (self.current_move["order"] == "b"):
            inter_string += " ..."

        inter_string += "\n" + " " * (self.space_counter_in_line(self.current_move["line"]) + self.tab_len)
        move_line = self.current_move["line"] + 1

        inter_string += str(self.current_move["move"]) + ')'

        if (self.current_move["order"] == "b"):
            inter_string += "..."

        inter_string += move_rec
        if self.current_move["order"] == "b":
            inter_string += "\n"
        if (self.current_move["order"] == "w") and (current_line.startswith(' ')):
            inter_string += "\n"
        inter_string += " " * (self.space_counter_in_line(self.current_move["line"]))

        if self.current_move["order"] == 'b':
            inter_string += str(self.current_move["move"]) + ')...'

        if (inter_string.startswith(" ...")) and (inter_string.endswith("...")) and (current_line.endswith("...")):
            inter_string = "\n" + inter_string.split("\n")[1]
            self.insert("{}.{}".format(self.current_move["line"], right_space + 4), inter_string)
        else:
            self.insert("{}.{}".format(self.current_move["line"], right_space), inter_string)
        return move_line

    def compose_inter_string_not_carriyng(self, move_rec, right_space):

        inter_string = ""
        current_line = self.lines[self.current_move["line"]]

        print("CURRENT LINE", current_line)

        move_line = self.current_move["line"]

        if self.current_move["order"] == "w":
            inter_string += (" " + str(self.current_move["move"]) + ')')
        else:
            inter_string += " "

        inter_string += move_rec

        print("INTER_STRING", inter_string)
        # NEED TO INSERT INTER_STRING
        self.insert("{}.{}".format(self.current_move["line"], right_space), inter_string)
        return move_line

    def highlight_move(self, line_num: int, char_num: int) -> None:

        if char_num >= len(self.lines[line_num]):
            char_num = len(self.lines[line_num]) - 1

        current_line = self.lines[line_num]
        if len(current_line) == 0:
            return

        left_space, right_space = self.get_left_and_right_space_around_char_num(line_num, char_num)

        self.tag_delete("black")
        self.tag_config("black", background="black", foreground="white")
        self.tag_add("black", "{}.{}".format(line_num, left_space + 1), "{}.{}".format(line_num, right_space))
        self.reposition_current_move(line_num, left_space, right_space)
        return left_space

    def get_fen_after_move(self, line_num, left_space_index):
        left_part = self.lines[line_num][:left_space_index + 1]
        space_count = self.span_spaces_at_start(left_part).count(" ")
        if "... " in left_part:
            space_count -= 1

        print("LINES HERE")
        for line in self.lines:
            print(line)

        print("LINES AND FENS HERE")
        for line in self.lines_and_fens:
            print(line)
        return self.lines_and_fens[line_num][space_count]["fen"]

    def go_to_move(self, event):
        self.update_moves_lines()
        line_num, char_num = [int(index) for index in self.index("current").split('.')]
        left_space_index = self.highlight_move(line_num, char_num)
        fen_to_set = Fen.Fen(self.get_fen_after_move(line_num, left_space_index))
        boart_to_set = fen_to_set.fen_to_board()
        return boart_to_set
        #fen_to_set.fen_to_board().print_position_as_text_from_white()

    def current_move_is_main(self):
        print(self.current_move["order"] == 'b')
        print(len(self.lines) - 1 == self.current_move["line"])
        print(' ' not in self.lines[self.current_move["line"]])
        print((self.current_move["line"] == 1) or (' ' not in self.lines[self.current_move["line"]]))
        #print(len(self.lines), self.current_move["line"])
        return ((self.current_move["order"] == 'w') and (len(self.lines) == self.current_move["line"] + 1)) or \
            ((self.current_move["order"] == 'b') and (len(self.lines) - 1 == self.current_move["line"]) and ((self.current_move["line"] == 1) or (' ' not in self.lines[self.current_move["line"]])))

    def record_a_move(self, move_note, fen_after_move):

        if self.current_move_is_main():
            move_line = self.base_record_move(move_note, fen_after_move)
        else:
            move_line = self.side_record_move(move_note, fen_after_move)

        print("LINES AND FENS HERE")
        for line in self.lines_and_fens:
            print(line)

        #print("MOVE_LINE", move_line)
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
