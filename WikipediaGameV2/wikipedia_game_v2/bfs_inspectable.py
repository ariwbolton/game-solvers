from typing import Literal

from wikipedia_game_v2.page import Page
from wikipedia_game_v2.page_loader import PageLoader


class BFSInspectable:
    def __init__(self, *, start: Page, end: Page, direction: Literal["forward", "backward"], page_loader: PageLoader):
        self.page_loader = page_loader
        self.direction = direction
        self.start: Page = start
        self.end: Page = end
        self.current = set(self._get_links(start))
        self.seen = set(self.current)
        self.prevs = {link: self.start.id for link in self.current}

    def step(self):
        if self.is_finished():
            raise Exception('Cannot step because BFS has already finished')

        pages = self.page_loader.load_pages(pageids=list(self.current))

        self.current = set()

        for page in pages:
            for link in self._get_links(page):
                if link in self.seen:
                    continue

                self.current.add(link)
                self.seen.add(link)
                self.prevs[link] = page.id

    def is_finished(self):
        return self.end.id in self.current

    def path(self, target: int) -> list[int] | None:
        """Get path from start to target"""
        path = []
        current = target

        while current != self.start.id:
            path.append(current)

            if current not in self.prevs:
                return None

            current = self.prevs[current]

        return list(reversed(path))

    def _get_links(self, page: Page):
        return page.links if self.direction == 'forward' else page.backlinks
