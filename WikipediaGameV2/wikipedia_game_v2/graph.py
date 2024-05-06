from wikipedia_game_v2.page import Page
from wikipedia_game_v2.page_loader import PageLoader


class Graph:
    """Each node is a page, and edges are links"""

    def __init__(self, page_loader: PageLoader):
        self._pages: list[Page] = []
        self.page_loader = page_loader

    def page(self, *, pageid: int, name: str) -> Page:
        """Returns a Page object. Fetches first, if needed, using page_loader."""
        pass

    def pages(self, *, pageids: list[int]) -> list[Page]:
        pass


