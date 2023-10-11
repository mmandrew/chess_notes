import Board
import Fen
from Bishop import Bishop as b
from Knight import Knight as n
from Rook import Rook as r
from Queen import Queen as q
from Pawn import Pawn as p
from King import King as k
import Move
from tkinter import *
from PIL import ImageTk, Image
import chessCanvas

board = Board.Board()
#board.draw_empty_board()
#board.set_start_position()
#board.print_position_as_text()
"""
fen = Fen.Fen("1k6/p6p/3P4/5P2/4B3/8/1P4PK/8 w - - 0 1")
board = fen.fen_to_board()
board.print_position_as_text_from_white()
print(board.board_to_fen())
print(b.check_move_legal(start_square=board.board[3][4], end_square=board.board[0][7], board=board))
print(b.check_move_legal(start_square=board.board[3][4], end_square=board.board[4][5], board=board))
print(b.check_move_legal(start_square=board.board[3][4], end_square=board.board[5][6], board=board))
print(b.check_move_legal(start_square=board.board[3][4], end_square=board.board[6][1], board=board))
print(b.check_move_legal(start_square=board.board[2][4], end_square=board.board[0][7], board=board))
print(b.check_move_legal(start_square=board.board[3][4], end_square=board.board[2][3], board=board))
"""

"""
fen = Fen.Fen("1k6/p7/3P1p2/5P2/4N3/8/1P4PK/8 w - - 0 1")
board = fen.fen_to_board()
board.print_position_as_text_from_white()
print(board.board_to_fen())
print(n.check_move_legal(start_square=board.board[3][4], end_square=board.board[5][3], board=board))
print(n.check_move_legal(start_square=board.board[3][4], end_square=board.board[5][5], board=board))
print(n.check_move_legal(start_square=board.board[3][4], end_square=board.board[3][1], board=board))
print(n.check_move_legal(start_square=board.board[3][4], end_square=board.board[4][3], board=board))
"""

"""
fen = Fen.Fen("1k6/p7/4p3/5P2/Pp2R2P/8/1P6/6K1 w - - 0 1")
board = fen.fen_to_board()
board.print_position_as_text_from_white()
print(r.check_move_legal(start_square=board.board[3][4], end_square=board.board[3][6], board=board)) #True
print(r.check_move_legal(start_square=board.board[3][4], end_square=board.board[3][7], board=board)) #False
print(r.check_move_legal(start_square=board.board[3][4], end_square=board.board[3][1], board=board)) #True
print(r.check_move_legal(start_square=board.board[3][4], end_square=board.board[3][0], board=board)) #False
print(r.check_move_legal(start_square=board.board[3][4], end_square=board.board[3][2], board=board)) #True
print(r.check_move_legal(start_square=board.board[3][4], end_square=board.board[5][4], board=board)) #True
print(r.check_move_legal(start_square=board.board[3][4], end_square=board.board[6][4], board=board)) #False
print(r.check_move_legal(start_square=board.board[3][4], end_square=board.board[7][4], board=board)) #False
print(r.check_move_legal(start_square=board.board[3][4], end_square=board.board[0][4], board=board)) #True
print(r.check_move_legal(start_square=board.board[3][4], end_square=board.board[7][5], board=board)) #False
"""

"""
fen = Fen.Fen("1k6/pp6/4p3/5P2/Pp2Q2P/8/1PP5/6K1 w - - 0 1")
board = fen.fen_to_board()
board.print_position_as_text_from_white()
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[3][6], board=board)) #True
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[3][7], board=board)) #False
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[3][1], board=board)) #True
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[3][0], board=board)) #False
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[3][2], board=board)) #True
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[5][4], board=board)) #True
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[6][4], board=board)) #False
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[7][4], board=board)) #False
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[0][4], board=board)) #True
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[7][5], board=board)) #False

print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[6][1], board=board)) #True
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[7][0], board=board)) #False
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[4][5], board=board)) #False
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[0][1], board=board)) #False
print(q.check_move_legal(start_square=board.board[3][4], end_square=board.board[1][2], board=board)) #False
"""

"""
fen = Fen.Fen("r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4")
board = fen.fen_to_board()
board.print_position_as_text_from_white()
print(board.square_attacked_by_white(board.board[7][6]))
"""

"""
fen = Fen.Fen("8/5k2/8/5p2/6K1/8/r1B5/8 b - - 0 1")
board = fen.fen_to_board()
board.print_position_as_text_from_white()
print(board.white_king_in_check())
print(board.black_king_in_check())
"""

"""
fen = Fen.Fen("r3k2r/8/8/8/2B5/8/1p6/R3K2R w KQkq - 0 1")
board = fen.fen_to_board()
board.print_position_as_text_from_white()
print(k.check_move_legal(start_square=board.board[0][4], end_square=board.board[0][6], board=board)) #True
print(k.check_move_legal(start_square=board.board[0][4], end_square=board.board[0][2], board=board)) #False
print(k.check_move_legal(start_square=board.board[0][4], end_square=board.board[0][3], board=board)) #True
print(k.check_move_legal(start_square=board.board[0][4], end_square=board.board[1][5], board=board)) #True
print(k.check_move_legal(start_square=board.board[0][4], end_square=board.board[2][6], board=board)) #False
print(k.check_move_legal(start_square=board.board[7][4], end_square=board.board[7][6], board=board)) #False
print(k.check_move_legal(start_square=board.board[7][4], end_square=board.board[7][2], board=board)) #True
print(k.check_move_legal(start_square=board.board[7][4], end_square=board.board[5][6], board=board)) #False
print(k.check_move_legal(start_square=board.board[7][4], end_square=board.board[6][5], board=board)) #False
"""

"""
fen = Fen.Fen("r3k2r/8/8/4Pp2/1PB5/8/1p3P2/R3K2R w KQkq f6 0 2")
board = fen.fen_to_board()
board.print_position_as_text_from_white()
print(p.check_move_legal(start_square=board.board[3][1], end_square=board.board[4][1], board=board)) #True
print(p.check_move_legal(start_square=board.board[3][1], end_square=board.board[4][2], board=board)) #False
print(p.check_move_legal(start_square=board.board[3][1], end_square=board.board[5][1], board=board)) #False
print(p.check_move_legal(start_square=board.board[1][5], end_square=board.board[2][5], board=board)) #True
print(p.check_move_legal(start_square=board.board[1][5], end_square=board.board[3][5], board=board)) #True
print(p.check_move_legal(start_square=board.board[4][4], end_square=board.board[5][5], board=board)) #True
print(p.check_move_legal(start_square=board.board[4][4], end_square=board.board[5][4], board=board)) #True
print(p.check_move_legal(start_square=board.board[4][4], end_square=board.board[6][4], board=board)) #False
"""

"""
fen = Fen.Fen("kb2r3/8/6pp/PpPpNP2/2p5/7p/7P/RQ2K2R w KQ b6 0 1")
board = fen.fen_to_board()
board.print_position_as_text_from_white()
print(Move.Move.check_move_legal(board.board[0][4], board.board[0][6], board)) #True
print(Move.Move.check_move_legal(board.board[0][4], board.board[0][2], board)) #False
print(Move.Move.check_move_legal(board.board[0][4], board.board[1][3], board)) #True
print(Move.Move.check_move_legal(board.board[4][4], board.board[5][7], board)) #False
print(Move.Move.check_move_legal(board.board[0][1], board.board[2][2], board)) #False
print(Move.Move.check_move_legal(board.board[4][5], board.board[6][5], board)) #False
print(Move.Move.check_move_legal(board.board[4][5], board.board[5][5], board)) #True
print(Move.Move.check_move_legal(board.board[4][5], board.board[5][6], board)) #True
print(Move.Move.check_move_legal(board.board[4][5], board.board[5][4], board)) #False
print(Move.Move.check_move_legal(board.board[4][0], board.board[5][1], board)) #True
print(Move.Move.check_move_legal(board.board[4][0], board.board[5][1], board)) #True
print(Move.Move.check_move_legal(board.board[4][2], board.board[5][1], board)) #True
print(Move.Move.check_move_legal(board.board[4][2], board.board[5][3], board)) #False
print(Move.Move.check_move_legal(board.board[0][1], board.board[4][1], board)) #True
print(Move.Move.check_move_legal(board.board[1][7], board.board[3][7], board)) #False
print(Move.Move.check_move_legal(board.board[1][7], board.board[2][7], board)) #False
"""

"""
fen = Fen.Fen("kb2r3/8/6pp/PpPpNP2/2p5/8/7P/RQ2K2R w KQ b6 0 1")
board = fen.fen_to_board()
board.print_position_as_text_from_white()
#print(board.castles.white_kingside_castle_possible)
#r.do_move(board.board[0][7], board.board[0][6], board)
#Move.Move.do_move(board.board[1][7], board.board[3][7], board)
Move.Move.do_move(board.board[0][1], board.board[4][1], board)
print("MOVE DONE")
board.print_position_as_text_from_white()
#print(board.castles.white_kingside_castle_possible)

#board = Board.Board()
#oard.print_position_as_text_from_white()
#print(id(board.board[0][0]), id(board.board[0][1]))
#Move.Move.simple_move(board.board[0][0], board.board[0][1], board)
#print(id(board.board[0][0]), id(board.board[0][1]))
"""

#board.draw_empty_board()

#window = Tk()
#window.title("Chess notes")
#window.geometry("1200x605")
#window.update_idletasks()

"""
fen = Fen.Fen("8/8/8/8/8/8/8/Q7 w - -")
board = fen.fen_to_board()
board.print_position_as_text_from_white()

chess_canvas = chessCanvas.chessCanvas(window)
chess_canvas.set_canvas_board(board)
chess_canvas.draw_piece_on_board('Q', board.board[0][0])

img = ImageTk.PhotoImage(Image.open("../assets/board_image_1.png"))
b = chess_canvas.canvas.create_image(300, 305, anchor="center", image=img)
chess_canvas.window.mainloop()
"""

chess_canvas = chessCanvas.chessCanvas()
#chess_canvas.draw_empty_board()
chess_canvas.mainloop()



#canvas = Canvas(window, width=600, height=605)
#canvas.pack()
#img = ImageTk.PhotoImage(Image.open("../assets/board_image_1.png"))
#b = canvas.create_image(300, 305, anchor="center", image=img)
#window.mainloop()









