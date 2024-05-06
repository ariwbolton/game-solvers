import os

import httpx
import requests
import requests_cache

from wikipedia_game_v2.constants import DATA_DIR

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

# Sample URLs

# Load links + backlinks for a list of pages, by page ID, in JSON
# https://en.wikipedia.org/w/api.php?action=query&pageids=12345|67890&prop=links|linkshere&pllimit=max&lhlimit=max&format=json

# Load rich links (which include both a pageid and name) for a list of pages
# https://en.wikipedia.org/w/api.php?action=query&generator=links&pageids=12345&gpllimit=max&prop=info&format=json

class WikipediaAPI:
    """Cached Wikipedia API wrapper

    Stores request responses indefinitely, because this is just a toy project and doesn't need to be up-to-date
    """

    client: httpx.AsyncClient = None

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

        self.client.headers = {
            'User-Agent': 'Ari Bolton\'s Wikipedia game solver (ariwbolton@gmail.com)'
        }

    ########
    # Core #
    ########

    async def query_simple(self, *, pageids: list[int], prop: list[str] | str, format: str = 'json') -> dict:
        params = {
            "action": "query",
            "pageids": "|".join(str(pageid) for pageid in pageids),
            "prop": "|".join(prop) if isinstance(prop, list) else prop,
            "format": format,

            # "prop links" parameters
            "pllimit": "max",
            "plnamespace": '0|4',  # limit to "Main" and "Wikipedia" namespaces (https://en.wikipedia.org/wiki/Help:MediaWiki_namespace)

            # "links here" parameters
            "lhlimit": "max",
            "lhnamespace": '0|4',
        }

        print('Fetching simple query')

        r = await self.client.get(WIKIPEDIA_API_URL, params=params)

        print(r.url)

        result = r.json()

        full_query_pages = result['query']['pages']

        while 'continue' in result:
            print('Paginating simple query')
            r = await self.client.get(WIKIPEDIA_API_URL, params={**params, **result['continue']})

            print(r.url)

            result = r.json()

            result_pages = result['query']['pages']

            for key in set(full_query_pages.keys()) | set(result_pages.keys()):
                full_query_pages[key] = self._merge_page_results(full_query_pages.get(key, None), result_pages.get(key, None))

        return full_query_pages


    def _merge_page_results(self, a, b) -> dict:
        if not a:
            return b

        if not b:
            return a

        return {
            **a,
            'links': a.get('links', []) + b.get('links', []),
            'linkshere': a.get('linkshere', []) + b.get('linkshere', [])
        }

    async def query_links_generator(self, *, pageids: list[int], prop: str, format: str = 'json') -> dict:
        params = {
            "action": "query",
            "pageids": "|".join(str(pageid) for pageid in pageids),
            "generator": 'links',
            "prop": prop,
            "format": format,

            # "prop links" parameters
            "gpllimit": "max",
            "gplnamespace": "0|4" # limit to "Main" and "Wikipedia" namespaces (https://en.wikipedia.org/wiki/Help:MediaWiki_namespace)
        }

        print('Fetching links generator')

        r = await self.client.get(WIKIPEDIA_API_URL, params=params)

        print(r.url)

        result = r.json()

        all_links = result['query']['pages']

        while 'continue' in result:
            print('Paginating links generator')
            r = await self.client.get(WIKIPEDIA_API_URL, params={**params, **result['continue']})

            print(r.url)

            result = r.json()

            all_links.update(result['query']['pages'])

        return all_links

