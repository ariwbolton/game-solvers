"""Graph and Node class module"""
import copy
import itertools

from .group import Group


class Node:
    """Node class

    Represents a node in the bipartite graph. At the time of writing, can either be a "Number" or a "Cell"
    """

    def __init__(self, value):
        """Initialize the node

        :param int|Cell value: Either a "number" or a "cell"
        """
        self.value = value


class Edge:
    """Edge class"""

    def __init__(self, cell, number):
        self.cell = cell
        self.number = number

        self.tup = (self.cell, self.number)

    def __repr__(self):
        return f'Edge({self.cell}, {self.number})'

    def __hash__(self):
        return hash(self.tup)

    def __lt__(self, other):
        return self.tup < other.tup


class Graph:
    """Graph class

    Maintains a bipartite graph of "numbers" and "cells"
    """

    def __init__(self, board):
        self.board = board

        # Maintain mapping from cells to numbers
        self.edges = {}

        for cell in self.board.all_cells:
            if cell.value is None:
                self.edges[cell] = Group(self.board.numbers)
            else:
                self.edges[cell] = Group([cell.value])

    def remove_edge(self, edge):
        """Remove an edge from the graph"""
        return self.remove_edges([edge])

    def remove_edges(self, edges):
        """Remove a set of edges from the graph

        :returns: The list of constraints that have been updated, and should be re-checked
        """
        removed_edge_set = set()
        constraints_to_update = set()
        constraint_list = list()

        print("Removing edges", edges)

        for edge in edges:
            cell, number = edge.cell, edge.number

            if edge in removed_edge_set:
                print("Attempting to remove duplicate edge", edge, 'skipping...')
                continue

            print(f"Removing edge {edge}")
            removed_edge_set.add(edge)

            # Remove the edge
            if number not in self.edges[cell]:
                print(f"Spurious `remove_edge`: {number} from {cell} options: {self.edges[cell]}")
                continue

            self.edges[cell].remove(number)

            if len(self.edges[cell]) == 1:
                print("Cell identified!", cell, self.edges[cell][0])

            for constraint in cell.constraints:
                if constraint not in constraints_to_update:
                    constraints_to_update.add(constraint)
                    constraint_list.append(constraint)

        # Update constraints
        for constraint in constraint_list:
            constraint.update()

        return constraint_list
