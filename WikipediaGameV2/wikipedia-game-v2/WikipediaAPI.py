import requests

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

# Sample URLs

# Load links + backlinks for a list of pages, by page ID, in JSON
# https://en.wikipedia.org/w/api.php?action=query&pageids=12345|67890&prop=links|linkshere&pllimit=max&lhlimit=max&format=json

# Load rich links (which include both a pageid and name) for a list of pages
# https://en.wikipedia.org/w/api.php?action=query&generator=links&pageids=12345&gpllimit=max&prop=info&format=json

class WikipediaAPI:

    ########
    # Core #
    ########

    def query_simple(self, *, pageids: list[int], prop: list[str] | str, format: str = 'json') -> dict:
        r = requests.get(WIKIPEDIA_API_URL, params={
            "action": "query",
            "pageids": "|".join(str(pageid) for pageid in pageids),
            "prop": "|".join(prop) if isinstance(prop, list) else prop,
            "format": format,
            "pllimit": "max",
            "hllimit": "max"
        })

        return r.json()

    def query_generator(self, *, pageids: list[int], generator: str, prop: str, format: str = 'json') -> dict:
        r = requests.get(WIKIPEDIA_API_URL, params={
            "action": "query",
            "pageids": "|".join(str(pageid) for pageid in pageids),
            "generator": generator,
            "prop": prop,
            "format": format,
            "gpllimit": "max",
        })

        return r.json()
