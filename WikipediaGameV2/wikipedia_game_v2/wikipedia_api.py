import os

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

    def __init__(self):
        self._session = requests_cache.CachedSession(
            os.path.join(DATA_DIR, 'http_cache'),
            backend='filesystem',
            expire_after=requests_cache.NEVER_EXPIRE,
            headers={
                'User-Agent': 'Ari Bolton\'s Wikipedia game solver (ariwbolton@gmail.com)'
            }
        )

    ########
    # Core #
    ########

    def query_simple(self, *, pageids: list[int], prop: list[str] | str, format: str = 'json') -> dict:
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

        r = requests.get(WIKIPEDIA_API_URL, params=params)

        result = r.json()

        full_query_pages = result['query']['pages']

        while 'continue' in result:
            print('continuing', result['continue'])
            r = requests.get(WIKIPEDIA_API_URL, params={**params, **result['continue']})

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

    def query_generator(self, *, pageids: list[int], generator: str, prop: str, format: str = 'json') -> dict:
        # TODO: Paginate through responses
        params = {
            "action": "query",
            "pageids": "|".join(str(pageid) for pageid in pageids),
            "generator": generator,
            "prop": prop,
            "format": format,
            "gpllimit": "max",
        }

        r = requests.get(WIKIPEDIA_API_URL, params=params)

        result = r.json()

        while 'continue' in result:
            print('continuing generator', result['continue'])
            r = requests.get(WIKIPEDIA_API_URL, params={**params, **result['continue']})

            result = r.json()

            # TODO: Finish this

