from Fen import Fen
import os
import pathlib

class ChessTree:
    def __init__(self, fen: Fen, moves: [] = []):
        self.fen = fen
        self.moves = moves

    def add_move(self, move, fen):
        self.moves[move] = ChessTree(fen)

    def print(self, tab_counter = 0):
        step = "  "
        print(step * tab_counter + self.fen)
        if len(self.moves) == 0:
            return
        print(step * tab_counter, self.moves[0])
        for move in self.moves[1:]:
            print(move)
            self.print(tab_counter + 1)

    def convert_to_text(self, info = [], tab_counter = 0):
        step = "  "
        info.append(step * tab_counter + self.fen)
        if len(self.moves) == 0:
            return info
        info.append(step * tab_counter, self.moves[0])
        for move in self.moves[1:]:
            info.append(move)
            self.print(info, tab_counter + 1)
        return info

    def start_space_length(line: str):
        counter = 0
        for c in line:
            if c == " ":
                counter += 1
            else:
                return counter

    def tree_from_file(self, path):
        file_path = pathlib.Path(__file__).parent.parent.resolve().joinpath("chess_trees\{}".format(path))
        with open(file_path, 'r') as f:
            lines = f.readlines()


        new_tree = ChessTree

        for line in lines:
            pass




if __name__ == "__main__":
    cn = ChessTree("kb2r3/8/6pp/PpPpNP2/2p5/7p/7P/RQ2K2R w KQ b6 0 1")
    cn.tree_from_file('abc')
