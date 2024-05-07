import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

# Sample URLs

# Load links + backlinks for a list of pages, by page ID, in JSON
# https://en.wikipedia.org/w/api.php?action=query&pageids=12345|67890&prop=links|linkshere&pllimit=max&lhlimit=max&format=json

# Load rich links (which include both a pageid and name) for a list of pages
# https://en.wikipedia.org/w/api.php?action=query&generator=links&pageids=12345&gpllimit=max&prop=info&format=json

class PopularPageException(Exception):
    def __init__(self, pageids: list[int]):
        super().__init__("Popular pages with many backlinks detected")
        self.pageids = pageids

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

    async def query_simple(self, *, prop: list[str] | str, format: str = 'json', pageids: list[int] = None, titles: list[str] = None) -> dict:
        params = {
            "action": "query",
            "prop": "|".join(prop) if isinstance(prop, list) else prop,
            "format": format,

            **({"pageids": "|".join(str(pageid) for pageid in pageids)} if pageids is not None else {}),
            **({"titles": "|".join(titles)} if titles is not None else {}),

            # "prop links" parameters
            **({
                # limit to "Main" namespaces (https://en.wikipedia.org/wiki/Help:MediaWiki_namespace)
                "pllimit": "max",

                # Categories 4 and 14 were attempted, but had some pages with so many linkshere that it's impossible to load
                # due to the API falling over
                "plnamespace": '0'
            } if 'links' in prop else {}),

            # "links here" parameters
            **({
                "lhlimit": "max",
                "lhnamespace": '0'
            } if 'linkshere' in prop else {}),
        }

        print('Fetching simple query')

        result = await self._request(params, diagnostics=True)

        full_query_pages = result['query']['pages']

        while 'continue' in result:
            result = await self._request({**params, **result['continue']}, diagnostics=True)

            result_pages = result['query']['pages']

            for key in set(full_query_pages.keys()) | set(result_pages.keys()):
                full_query_pages[key] = self._merge_page_results(full_query_pages.get(key, None), result_pages.get(key, None))

            # Some pages have a ridiculous number of backlinks, and will take far too long to finish
            # Other strategies must be used to work around those missing backlinks
            long_backlinks_results = [result for result in full_query_pages.values() if 'linkshere' in result and len(result["linkshere"]) > 10000]

            if long_backlinks_results:
                raise PopularPageException(pageids=[result["pageid"] for result in long_backlinks_results])

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

    @retry(retry=retry_if_exception_type(httpx.ReadTimeout), stop=stop_after_attempt(5))
    async def _request(self, params, diagnostics=False) -> dict:
        try:
            r = await self.client.get(WIKIPEDIA_API_URL, params=params, timeout=15.0)

            if diagnostics:
                print(r.elapsed, r.url)

            return r.json()
        except httpx.ReadTimeout as e:
            print('ReadTimeout URL:', str(e.request.url))
            raise e
        except Exception as e:
            print('uh oh!')
            raise e


