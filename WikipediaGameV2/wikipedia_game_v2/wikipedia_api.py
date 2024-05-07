import httpx
from httpx import Response
from tenacity import retry, retry_if_exception_type, stop_after_attempt

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
            "plnamespace": '0',  # limit to "Main" namespaces (https://en.wikipedia.org/wiki/Help:MediaWiki_namespace)
            # Categories 4 and 14 were attempted, but had some pages with so many linkshere that it's impossible to load
            # due to the API falling over

            # "links here" parameters
            "lhlimit": "max",
            "lhnamespace": '0',
        }

        print('Fetching simple query')

        result = await self._request(params, diagnostics=True)

        full_query_pages = result['query']['pages']

        while 'continue' in result:
            result = await self._request({**params, **result['continue']})

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
            "gplnamespace": "0" # limit to "Main" namespace (https://en.wikipedia.org/wiki/Help:MediaWiki_namespace)
        }

        print('Fetching links generator')

        result = await self._request(params, diagnostics=True)

        all_links = result['query']['pages']

        while 'continue' in result:
            result = await self._request({**params, **result['continue']})

            all_links.update(result['query']['pages'])

        return all_links

    @retry(retry=retry_if_exception_type(httpx.ReadTimeout), stop=stop_after_attempt(10))
    async def _request(self, params, diagnostics=False) -> dict:
        try:
            r = await self.client.get(WIKIPEDIA_API_URL, params=params, timeout=6.0)

            if diagnostics:
                print(r.elapsed, r.url)

            return r.json()
        except httpx.ReadTimeout as e:
            print('ReadTimeout URL:', str(e.request.url))
            raise e
        except Exception as e:
            print('uh oh!')
            raise e


