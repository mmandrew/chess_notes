import Consts

class Piece:
    def __init__(self, name, color):
        if name not in Consts.piece_set:
            raise NameError("{} is WRONG piece!".format(name))
        self.name = name
        #self.line = line
        #self.rank = rank
        if color not in Consts.color_set:
            raise NameError("{} is WRONG color!".format(color))
        self.color = color

    def copy_self(self):
        new_p = Piece(self.name, self.color)

        return new_p

    def move(self):
        pass

    def take(self):
        pass

    def remove(self):
        pass

    def print_piece(self):
        print("name", self.name, "color", self.color, end="")

if __name__ == "__main__":
    pass