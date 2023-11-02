class Castles:
    def __init__(self):
        self.white_kingside_castle_possible = False
        self.white_queenside_castle_possible = False
        self.black_kingside_castle_possible = False
        self.black_queenside_castle_possible = False

    def set_white_kingside_castle_possible(self):
        self.white_kingside_castle_possible = True

    def set_white_queenside_castle_possible(self):
        self.white_queenside_castle_possible = True

    def set_black_kingside_castle_possible(self):
        self.black_kingside_castle_possible = True

    def set_black_queenside_castle_possible(self):
        self.black_queenside_castle_possible = True

    def set_white_kingside_castle_impossible(self):
        self.white_kingside_castle_possible = False

    def set_white_queenside_castle_impossible(self):
        self.white_queenside_castle_possible = False

    def set_black_kingside_castle_impossible(self):
        self.black_kingside_castle_possible = False

    def set_black_queenside_castle_impossible(self):
        self.black_queenside_castle_possible = False

    def set_castles_by_fen(self, castles: str):
        if "K" in castles:
            self.set_white_kingside_castle_possible()
        else:
            self.set_white_kingside_castle_imossible()
        if "Q" in castles:
            self.set_white_queenside_castle_possible()
        else:
            self.set_white_queenside_castle_impossible()
        if "k" in castles:
            self.set_black_kingside_castle_possible()
        else:
            self.set_black_kingside_castle_impossible()
        if "q" in castles:
            self.set_black_queenside_castle_possible()
        else:
            self.set_black_queenside_castle_impossible()

    def print_castles(self):
        if self.white_kingside_castle_possible:
            print('K', end='')
        if self.white_queenside_castle_possible:
            print('Q', end='')
        if self.black_kingside_castle_possible:
            print('k', end='')
        if self.black_queenside_castle_possible:
            print('q', end='')
        print()


if __name__ == "__main__":
    pass
