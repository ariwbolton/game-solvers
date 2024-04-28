import unittest

from wikipedia_game_v2.WikipediaAPI import WikipediaAPI


class TestWikipediaAPI(unittest.TestCase):

    def test_query_simple(self):
        wikipedia = WikipediaAPI()

        result = wikipedia.query_simple(pageids=[12345], prop=['links', 'linkshere'])

        print(result)