"""Group classes"""
import itertools

from .cell import Cell
from .graph import Edge
from .group import Group


class Constraint:
    """Constraint class

    Maintains a reference to cells affected by this constraint
    """

    #: Type of constraint
    subclass = None
    subclass_order = {
        'row': 0,
        'col': 1,
        'region': 2
    }

    def __init__(self, board, index):
        self.board = board
        self.index = index
        self.cells = list()   # Overridden by subclasses

        self._retrieve_cells()
        self.cell_set = set(self.cells)

        # Register constraints in cells
        for cell in self.cells:
            cell.register_constraint(self)

        # Create constant cell mapping
        # This means that the graph should only ever modify edge lists IN-PLACE
        # Creating new lists will break this!
        self.cell_options = {cell: self.board.graph.edges[cell] for cell in self.cells}

        self.update()

    def _retrieve_cells(self):
        """Create cells"""
        raise NotImplementedError("`create_cells` is not implemented!")

    def __hash__(self):
        return hash((self.subclass,) + tuple(self.cells))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.index})'

    def __lt__(self, other):
        return (Constraint.subclass_order[self.subclass], self.cells) < (Constraint.subclass_order[other.subclass], other.cells)

    def numbers(self):
        """Get currently inputted values for this constraint"""
        return set(c.value for c in self.cells) - {None}

    @property
    def number_options(self):
        """Get the mapping from numbers to cells, for this constraint

        (key, cell_group) => "key" must be in one of the cells in cell_group
        """
        mapping = {n: Group() for n in self.board.numbers}

        for cell, number_group in self.cell_options.items():
            for number in number_group:
                mapping[number].add(cell)

        return mapping

    @property
    def cell_group_options(self):
        """Mapping from cell groups to number group

        (cell_group, number_group) => cell_group must contain number_group
        """
        mapping = {}

        for cell, number_options in self.cell_options.items():
            if number_options not in mapping:
                mapping[number_options] = Group()

            mapping[number_options].add(cell)

        # Invert mapping back to correct format
        return {v: k for k, v in mapping.items()}

    @property
    def number_group_options(self):
        """Mapping from number groups to cell group

        (number_group, cell_group) => number group must be in cell_group
        """
        mapping = {}

        for number, cell_options in self.number_options.items():
            if cell_options not in mapping:
                mapping[cell_options] = Group()

            mapping[cell_options].add(number)

        # Invert mapping back to correct format
        return {v: k for k, v in mapping.items()}

    def update(self):
        """Update important attributes"""
        # TODO: Determine if we actually need to use this, because maps are dynamic
        pass

    def enforce(self):
        """Update the graph using this constraint.

        Returns a list of constraints that should be re-checked"""
        cell_group_options = self.cell_group_options
        number_group_options = self.number_group_options

        affected_cell_set = set()
        removals = set()

        for cell_group, number_group in cell_group_options.items():
            if len(cell_group) == len(number_group):
                # Numbers cannot appear anywhere else. Must trigger removal of those possibilities
                other_cells = sorted(self.cell_set - cell_group.items)
                # print(cell_group, 'must contain only', number_group, '. Removing', number_group, 'from', other_cells)

                for cell in other_cells:
                    for number in number_group:
                        if cell.can_contain(number):
                            affected_cell_set.add(cell)
                            removals.add(Edge(cell, number))

        for number_group, cell_group in number_group_options.items():
            if len(number_group) == len(cell_group):
                # These cells cannot contain any other numbers
                other_numbers = sorted(self.board.number_set - number_group.items)
                # print(number_group, 'can only be in', cell_group, '. Removing', other_numbers, 'from', cell_group)

                for cell in cell_group:
                    for number in other_numbers:
                        if cell.can_contain(number):
                            affected_cell_set.add(cell)
                            removals.add(Edge(cell, number))

        # Execute updates
        sorted_removals = sorted(removals)
        affected_constraints = self.board.graph.remove_edges(sorted_removals)

        # Generate constraints that should be re-checked
        # constraints = set()
        #
        # for cell in affected_cell_set:
        #     for constraint in cell.constraints:
        #         constraints.add(constraint)

        return affected_constraints


class RowConstraint(Constraint):
    """RowConstraint class"""

    subclass = 'row'

    def _retrieve_cells(self):
        """Create cell objects for this constraint. Called once during init."""
        self.cells = [self.board.cell(self.index, col_index) for col_index in range(0, self.board.n2)]


class ColConstraint(Constraint):
    """RowConstraint class"""

    subclass = 'col'

    def _retrieve_cells(self):
        """Create cell objects for this constraint. Called once during init."""
        self.cells = [self.board.cell(row_index, self.index) for row_index in range(0, self.board.n2)]


class RegionConstraint(Constraint):
    """RegionConstraint class

    Sample region indices for a 3-board:

     0 | 1 | 2
    --- --- ---
     3 | 4 | 5
    --- --- ---
     6 | 7 | 8
    """

    subclass = 'region'

    def _retrieve_cells(self):
        """Create cell objects for this constraint. Called once during init."""
        region_row_index = self.index // self.board.n
        region_col_index = self.index % self.board.n

        first_row = region_row_index * self.board.n
        first_col = region_col_index * self.board.n

        cells = []

        for region_index in range(0, self.board.n2):
            row_offset = region_index % self.board.n
            col_offset = region_index // self.board.n

            cells.append(self.board.cell(first_row + row_offset, first_col + col_offset))

        self.cells = cells
