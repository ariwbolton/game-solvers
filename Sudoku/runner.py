"""Sudoku Solver"""
from sudoku import Board


# Sample board names
# solved
# easy
# medium
# hard
# evil
# evil2

sample_board = Board.from_sample('evil2')

sample_board.print_board()
sample_board.solve()






