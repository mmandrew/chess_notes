from Fen import Fen

class ChessNode:
    def __init__(self, fen: Fen, moves: [] = []):
        self.fen = fen
        self.moves = moves

    def add_move(self, move, fen):
        self.moves[move] = ChessNode(fen)


if __name__ == "__main__":
    cn = ChessNode("kb2r3/8/6pp/PpPpNP2/2p5/7p/7P/RQ2K2R w KQ b6 0 1")