from wikipedia_game_v2.page import Page


class Graph:
    """Each node is a page, and edges are links"""

    def __init__(self, page_fetcher):
        self.pages: list[Page] = []
        self.page_fetcher = page_fetcher

    def page(self, *, pageid: int, name: str) -> Page:
        """Returns a Page object. Fetches first, if needed, using page_fetcher."""
        pass


