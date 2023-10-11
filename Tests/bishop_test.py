import Board
import Fen
from Bishop import Bishop as b

board = Board.Board()
#board.draw_empty_board()
#board.set_start_position()
#board.print_position_as_text()
fen = Fen.Fen("1k6/p6p/3P4/5P2/4B3/8/1P4PK/8 w - - 0 1")

board = fen.fen_to_board()
board.print_position_as_text_from_white()

print(b.check_move_legal(end_square=board.board[0][7], board=board))
print(b.check_move_legal(end_square=board.board[4][5], board=board))
print(b.check_move_legal(end_square=board.board[5][6], board=board))
print(b.check_move_legal(end_square=board.board[6][1], board=board))
print(b.check_move_legal(end_square=board.board[0][7], board=board))
print(b.check_move_legal(end_square=board.board[2][3], board=board))
