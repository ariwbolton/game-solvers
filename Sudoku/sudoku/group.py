"""Group class module"""


class Group:
    """Record a set of items, and sort appropriately"""

    def __init__(self, items=None):
        self.items = set(items or [])

        self._compute_sorted()

    def _compute_sorted(self):
        """Update the internal sorted list"""
        self.items_sorted = tuple(sorted(list(self.items)))

    def add(self, item):
        """Add an item to the set"""
        self.items.add(item)

        self._compute_sorted()

    def remove(self, item):
        """Remove an item from the set"""
        self.items.remove(item)

        self._compute_sorted()

    @property
    def constraints(self):
        """If this is a Group of Cells, get all constraints that apply to all cells. Otherwise, throw."""
        if len(self.items_sorted) > 0 and isinstance(self.items_sorted[0], int):
            raise Exception(f"Attempting to access constraints of a Group that does not refer to cells: {self}")

        constraint_set_list = []

        for cell in self.items_sorted:
            cell_constraint_set = set(cell.constraints)

            constraint_set_list.append(cell_constraint_set)

        return set.intersection(*constraint_set_list)

    def __getitem__(self, key):
        return self.items_sorted[key]

    def __len__(self):
        return len(self.items)

    def __hash__(self):
        """Return the internal list of sorted items"""
        return hash(self.items_sorted)

    def __repr__(self):
        return f'Group<{self.items_sorted}>'

    def __contains__(self, item):
        return item in self.items

    def __eq__(self, other):
        return hash(self) == hash(other)
