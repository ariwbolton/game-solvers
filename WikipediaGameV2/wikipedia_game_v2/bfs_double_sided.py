from wikipedia_game_v2.bfs_inspectable import BFSInspectable
from wikipedia_game_v2.graph import Graph, Page


class BFSDoubleSided:
    def __init__(self, graph: Graph):
        self.graph = graph

    def search(self, start: Page, end: Page) -> list[Page] | None:
        """Iterate forward from the start, AND backwards from the end, using the less costly side aat each step"""
        if start.id == end.id:
            return [start]

        if end.id in start.links:
            return [start, end]

        forward = BFSInspectable(self.graph, start=start, end=end, direction='forward')
        backward = BFSInspectable(self.graph, start=end, end=start, direction='backward')

        while not (forward.current & backward.current) and forward.current and backward.current:
            if len(forward.current) <= len(backward.current):
                forward.step()
            else:
                backward.step()

        if not forward.current or not backward.current:
            return None

        # We've found a path!
        overlap = forward.current & backward.current
        pivot = overlap.pop()

        path = forward.path(pivot)[:-1] + [pivot] + list(reversed(backward.path(pivot)[:-1]))

        return self.graph.pages(pageids=path)
