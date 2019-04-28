"""Cell class module"""

from .graph import Edge


class Cell:
    """Records the coordinates of a cell, and other utility methods."""

    def __init__(self, board, row, col, constraints=None):
        """Save row and col, update coords"""
        self.board = board
        self.row = row
        self.col = col
        self.coords = (self.row, self.col)

        self.constraints = constraints or []
        self.constraints_map = {}

    @property
    def value(self):
        """Get value for this cell"""
        return self.board.values[self.row][self.col]

    def can_contain(self, number):
        """Determine if this cell can contain a number"""
        return self.board.graph.edge_exists(Edge(self, number))

    def register_constraint(self, constraint):
        """Register a constraint"""
        if constraint.subclass in self.constraints_map:
            raise Exception(f"Constraint type {constraint.subclass} already exists on {self}")

        self.constraints_map[constraint.subclass] = constraint
        self.constraints.append(constraint)

    def constraint(self, subclass):
        """Get a single constraint"""
        return self.constraints_map[subclass]

    @property
    def constraint_set(self):
        """Set of all constraints for this cell"""
        return set(self.constraints)

    @staticmethod
    def constraint_intersection(cell_group):
        """All constraints that contain these cells"""
        return set.intersection(*[cell.constraint_set for cell in cell_group])


    def __hash__(self):
        """Simply return coordinates for hashing"""
        return hash(self.coords)

    def __repr__(self):
        return f'Cell({self.row}, {self.col})'

    def __lt__(self, other):
        return self.coords < other.coords
