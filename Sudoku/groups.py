"""Group classes"""
import itertools


class Group:
    """Group class"""

    def __init__(self, board, index):
        self.board = board
        self.index = index

    def numbers(self):
        """Get values for this Group"""
        raise NotImplementedError("`values` is not implemented!")

    def value_set(self):
        """Get a set, with `None` removed"""
        # TODO: Rename
        return set(self.numbers()) - {None}


class RowGroup(Group):
    """RowGroup class"""

    def numbers(self):
        """Get values for this row"""
        return set(self.board.values[self.index, :])


class ColGroup(Group):
    """RowGroup class"""

    def numbers(self):
        """Get values for this row"""
        return set(self.board.values[:, self.index])


class SubsquareGroup(Group):
    """SubsquareGroup class

    Sample subsquare indices for a 3-board:

     0 | 1 | 2
    --- --- ---
     3 | 4 | 5
    --- --- ---
     6 | 7 | 8
    """

    def numbers(self):
        """Get values for this row"""
        subsquare_row_index, subsquare_col_index = self.board.subsquare_index_to_row_col(self.board)

        first_row = subsquare_row_index * self.board.n
        first_col = subsquare_col_index * self.board.n

        last_row = first_row + self.board.n
        last_col = first_col + self.board.n

        multiarray = self.board.values[first_row:last_row, first_col:last_col]

        return set([v for v in itertools.chain.from_iterable(multiarray)])
