"""Sudoku Solver"""
from sudoku import Board


# Sample board names
# solved
# easy
# medium
# hard
# evil
# evil2

easy = Board.from_sample('evil')

easy.print_board()
easy.solve()






