"""Board class"""
import copy
import itertools
import random

from . import util
from .groups import RowGroup, ColGroup, SubsquareGroup
from .options import CellOptions


class Board:
    """Board class"""

    #: Width of the square board in "major squares"
    n = None

    def __init__(self, values=None, n=None):
        """Initialize the board"""
        self.n = n or self.n or 3
        self.n2 = self.n * self.n

        if len(values) != self.n2:
            raise Exception(f'Board has {len(values)} rows, should have {self.n2}')

        for row in values:
            if len(row) != self.n2:
                raise Exception(f'Board has row of length {len(row)}, should be of length {self.n2}')

        self.values = copy.deepcopy(values)
        self.numbers = set(range(0, self.n))

        for row in self.values:
            for index, item in list(enumerate(row)):
                if not item:
                    row[index] = None

        self.groups = {
            'rows': [RowGroup(self, index) for index in range(0, self.n)],
            'cols': [ColGroup(self, index) for index in range(0, self.n)],
            'subsquares': [SubsquareGroup(self, index) for index in range(0, self.n)]
        }

        self.cell_options = [[CellOptions(self, row, col) for col in range(0, self.n)] for row in range(0, self.n)]

    def print_board(self):
        """Print the board."""
        string_board_nested_list = []
        max_item_length = 0
        max_subsquare_length = 0

        for row in self.values:
            string_row_list = []

            for row_subsquare_index, row_subsquare in enumerate(util.grouper(self.n, row)):
                subsquare_length = 0

                for item in row_subsquare:
                    used_item = item if item is not None else ' '

                    string_item = str(used_item)        # TODO(ari): Space correctly
                    string_row_list.append(string_item)

                    string_item_len = len(string_item)

                    # Update max item length
                    max_item_length = max(string_item_len, max_item_length)

                    # Update subsquare length
                    subsquare_length += string_item_len

                max_subsquare_length = max(max_subsquare_length, subsquare_length)

            string_board_nested_list.append(string_row_list)

        # Adjust each item to be the correct length by padding
        for row in string_board_nested_list:
            for item, index in list(enumerate(row)):
                row[index] = f'{item:{max_item_length}}'

        # Construct horizontal spacer
        gaps = [' '] * (self.n + 1)
        bars = '-' * (max_subsquare_length + self.n + 1)

        horizontal_spacer = bars.join(gaps)

        string_board_list = []

        for row_i, row in enumerate(string_board_nested_list):
            if row_i % self.n == 0:
                string_board_list.append(horizontal_spacer)

            row_string = '|'

            for subsquare in util.grouper(3, row):
                row_string += f' {" ".join(subsquare)} |'

            string_board_list.append(row_string)

        string_board_list.append(horizontal_spacer)

        print(*string_board_list, sep='\n')

    # Getters

    def row(self, i):
        """Get a row."""
        return self.groups['rows'][i]

    def col(self, i):
        """Get a col."""
        return self.groups['cols'][i]

    def subsquare(self, i):
        """Get a subsquare."""
        return self.groups['subsquares'][i]

    def cell(self, row, col):
        """Get a cell"""
        return self.values[row][col]

    def options(self, row, col):
        """Get CellOptions for a cell"""
        return self.cell_options[row][col]

    @property
    def rows(self):
        """Get an iterable of rows"""
        return self.groups['rows']

    @property
    def cols(self):
        """Get an iterable of cols"""
        return self.groups['rows']

    @property
    def subsquares(self):
        """Get an iterable of subsquares"""
        return self.groups['subsquares']

    # Setters

    def set_cell(self, row, col, val):
        """Set a cell"""
        self.values[row][col] = val

    # Util

    def row_col_to_subsquare_index(self, row, col):
        """Convert subsquare row and column indices to subsquare index"""
        return (row * self.n) + col

    def subsquare_index_to_row_col(self, subsquare_index):
        """Convert subsquare index to (row, col)

        Sample subsquare indices for a 3-board:

         0 | 1 | 2
        --- --- ---
         3 | 4 | 5
        --- --- ---
         6 | 7 | 8
        """
        subsquare_row_index = subsquare_index // self.n
        subsquare_col_index = subsquare_index % self.n

        return subsquare_row_index, subsquare_col_index


