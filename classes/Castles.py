class Castles:
    def __init__(self):
        self.white_kingside_castle_possible = True
        self.white_queenside_castle_possible = True
        self.black_kingside_castle_possible = True
        self.black_queenside_castle_possible = True

    def set_white_kingside_castle_possible(self):
        self.white_kingside_castle_possible = True

    def set_white_queenside_castle_possible(self):
        self.white_kingside_castle_possible = True

    def set_black_kingside_castle_possible(self):
        self.white_kingside_castle_possible = True

    def set_black_queenside_castle_possible(self):
        self.white_kingside_castle_possible = True

    def set_white_kingside_castle_impossible(self):
        self.white_kingside_castle_possible = False

    def set_white_queenside_castle_impossible(self):
        self.white_kingside_castle_possible = False

    def set_black_kingside_castle_impossible(self):
        self.white_kingside_castle_possible = False

    def set_black_queenside_castle_impossible(self):
        self.white_kingside_castle_possible = False

    def set_castles_by_fen(self, castles: str):
        if "K" in castles:
            self.set_white_kingside_castle_possible()
        if "Q" in castles:
            self.set_white_queenside_castle_possible()
        if "k" in castles:
            self.set_black_kingside_castle_possible()
        if "q" in castles:
            self.set_black_queenside_castle_possible()