"""Board class"""
import copy
import itertools
import queue

from . import util
from .cell import Cell
from .constraints import RowConstraint, ColConstraint, RegionConstraint
from .graph import Graph

from .boards import samples


class Board:
    """Board class"""

    #: Width of the square board in "regions"
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
        self.numbers = list(range(1, self.n2 + 1))
        self.number_set = set(self.numbers)
        self.cells = []

        # Create cells
        for row_index, row in enumerate(self.values):
            cell_row = []

            for col_index, item in list(enumerate(row)):
                if not item:
                    row[col_index] = None

                cell_row.append(Cell(self, row_index, col_index))

            self.cells.append(cell_row)

        # Initialize graph
        self.graph = Graph(self)

        # Initialize constraints
        # Depends on graph
        self.constraints = {
            'rows': [RowConstraint(self, index) for index in range(0, self.n2)],
            'cols': [ColConstraint(self, index) for index in range(0, self.n2)],
            'regions': [RegionConstraint(self, index) for index in range(0, self.n2)]
        }

    @staticmethod
    def from_sample(name):
        """Factory method to create from name of sample board"""
        if not hasattr(samples, name):
            print(f"Could not find sample board named {name}")
            return

        values = getattr(samples, name)

        return Board(values=values)

    def print_board(self):
        """Print the board."""
        string_board_nested_list = []
        max_item_length = 0
        max_region_length = 0

        for row in self.values:
            string_row_list = []

            for row_region_index, row_region in enumerate(util.grouper(self.n, row)):
                region_length = 0

                for item in row_region:
                    used_item = item if item is not None else ' '

                    string_item = str(used_item)
                    string_row_list.append(string_item)

                    string_item_len = len(string_item)

                    # Update max item length
                    max_item_length = max(string_item_len, max_item_length)

                    # Update region length
                    region_length += string_item_len

                max_region_length = max(max_region_length, region_length)

            string_board_nested_list.append(string_row_list)

        # Adjust each item to be the correct length by padding
        for row in string_board_nested_list:
            for index, item in list(enumerate(row)):
                row[index] = f'{item:{max_item_length}}'

        # Construct horizontal spacer
        gaps = [' '] * (self.n + 1)
        bars = '-' * (max_region_length + self.n + 1)

        horizontal_spacer = bars.join(gaps)

        string_board_list = []

        for row_i, row in enumerate(string_board_nested_list):
            if row_i % self.n == 0:
                string_board_list.append(horizontal_spacer)

            row_string = '|'

            for region in util.grouper(3, row):
                row_string += f' {" ".join(region)} |'

            string_board_list.append(row_string)

        string_board_list.append(horizontal_spacer)

        print(*string_board_list, sep='\n')

    def print_options(self):
        """Print debug info regarding options per cell"""
        print('---')
        for cell in sorted(list(self.graph.edges.keys())):
            print(f'{cell}: {self.graph.edges[cell]}')
        print('---')

    # Getters

    def row(self, i):
        """Get a row."""
        return self.constraints['rows'][i]

    def col(self, i):
        """Get a col."""
        return self.constraints['cols'][i]

    def region(self, i):
        """Get a region."""
        return self.constraints['regions'][i]

    def cell(self, row, col):
        """Get a cell"""
        return self.cells[row][col]

    def value(self, row, col):
        """Get a value"""
        return self.values[row][col]

    # def options(self, row, col):
    #     """Get CellOptions for a cell"""
    #     return self.cell_options[row][col]

    @property
    def rows(self):
        """Get an iterable of row constraints"""
        return self.constraints['rows']

    @property
    def cols(self):
        """Get an iterable of col constraints"""
        return self.constraints['rows']

    @property
    def regions(self):
        """Get an iterable of region constraints"""
        return self.constraints['regions']

    @property
    def all_cells(self):
        """Get an iterable of all cells"""
        return itertools.chain.from_iterable(self.cells)

    @property
    def solved(self):
        """Return whether or not the board is solved"""
        return all(cell.value is not None for cell in self.all_cells)

    # Setters

    def set_value(self, row, col, val):
        """Set a cell"""
        self.values[row][col] = val

    # SOLVE

    def solve(self):
        """Solve this sudoku!"""
        tasks = queue.Queue()
        task_set = set()

        # Initialize update mapping tasks
        for cell in self.all_cells:
            if cell.value is not None:
                for constraint in cell.constraints:
                    if constraint not in task_set:
                        tasks.put(constraint)
                        task_set.add(constraint)

        while not tasks.empty():
            constraint = tasks.get()
            task_set.remove(constraint)

            print('Updating', constraint)
            additional_tasks = constraint.enforce()

            nonexistant_additional_tasks = [task for task in additional_tasks if task not in task_set]

            print("additional tasks", nonexistant_additional_tasks)

            for task in nonexistant_additional_tasks:
                tasks.put(task)
                task_set.add(task)

        self.print_board()

        if self.solved:
            print("Success!")
        else:
            print("Unsolved.")

        return self
