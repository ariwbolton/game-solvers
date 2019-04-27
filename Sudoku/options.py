"""CellOptions class module"""


class CellOptions:
    """Util to manage the possibilities for a cell"""

    def __init__(self, board, row_index, col_index):
        self.board = board
        self.row = self.board.row(row_index)
        self.col = self.board.col(col_index)
        self.subsquare = self.board.subsquare()

    def get(self):
        """Get options for this cell"""
        invalid_options = self.row.numbers() | self.col.numbers() | self.subsquare.numbers()

        return self.board.numbers - invalid_options
