from wikipedia_game_v2.bfs_inspectable import BFSInspectable
from wikipedia_game_v2.graph import Graph, Page


class BFSDoubleSided:
    def __init__(self, graph: Graph):
        self.graph = graph

    def search(self, start: Page, end: Page) -> list[Page] | None:
        """Iterate forward from the start, AND backwards from the end, using the less costly side at each step"""
        if start.id == end.id:
            return [start]

        if end.id in start.links:
            return [start, end]

        forward = BFSInspectable(self.graph, start=start, end=end, direction='forward')
        backward = BFSInspectable(self.graph, start=end, end=start, direction='backward')

        step_count = 0
        forward_count = 0
        backward_count = 0

        while not (forward.current & backward.current) and forward.current and backward.current:
            step_count += 1

            print(f'Step {step_count}')
            print(f'Forward: {forward_count} steps, {len(forward.current)} nodes')
            print(f'Backward: {backward_count} steps, {len(backward.current)} nodes')

            if len(forward.current) <= len(backward.current):
                print('Stepping forwards...')
                forward_count += 1
                forward.step()
            else:
                print('Stepping backwards...')
                backward_count += 1
                backward.step()

            print('')

        if not forward.current or not backward.current:
            return None

        # We've found a path!
        overlap = forward.current & backward.current
        pivot = overlap.pop()

        path = forward.path(pivot)[:-1] + [pivot] + list(reversed(backward.path(pivot)[:-1]))

        return self.graph.pages(pageids=path)
