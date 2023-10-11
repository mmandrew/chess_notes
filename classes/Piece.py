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

    def move(self):
        pass

    def take(self):
        pass

    def remove(self):
        pass

if __name__ == "__main__":
    pass