

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

# https://en.wikipedia.org/w/api.php?action=query&pageids=12345|67890|55555|55|555|5555|1111|11111|1111&prop=links|linkshere&pllimit=max&lhlimit=max&format=json

class WikipediaAPI:
    def query(self, *, pageids: list[int], prop: list[str] | str, format: str = 'json') -> dict:
        pass