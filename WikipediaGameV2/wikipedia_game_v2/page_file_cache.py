import json
import os

from wikipedia_game_v2.constants import DATA_DIR
from wikipedia_game_v2.page import Page


class PageFileCache:
    def __init__(self):
        self.dir = os.path.join(DATA_DIR, 'page_cache')

    def setup(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def get(self, pageid: int) -> Page | None:
        filename = self.filename(pageid)

        if not os.path.isfile(filename):
            return None

        try:
            with open(filename, 'r') as f:
                page_json = json.load(f)

            return Page.from_dict(page_json)
        except Exception as e:
            # TODO: Add better logging

            print('Could not load page JSON')

            return None

    def store(self, page: Page):
        """Overwrites any existing files"""
        filename = self.filename(page.id)

        page_json = page.to_dict()

        with open(filename, 'w+') as f:
            json.dump(page_json, f)

    def filename(self, pageid: int) -> str:
        return os.path.join(self.dir, str(pageid))

