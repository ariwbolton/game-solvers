from wikipedia_game_v2.graph import Graph, Page


class DoubleSidedBFSSearch:
    def __init__(self, graph: Graph):
        self.graph = graph

    def search(self, start: Page, end: Page) -> list[Page]:
        pass