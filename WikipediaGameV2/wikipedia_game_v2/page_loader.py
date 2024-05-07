import asyncio

from pydash import chunk, key_by, compact

from wikipedia_game_v2.page import Page
from wikipedia_game_v2.page_file_cache import PageFileCache
from wikipedia_game_v2.wikipedia_api import WikipediaAPI, PopularPageException


class PageLoader:
    def __init__(self, wikipedia_api: WikipediaAPI):
        self.wikipedia_api = wikipedia_api
        self.page_file_cache = PageFileCache()

        self.page_file_cache.setup()

    async def load_pages(self, *, pageids: list[int]) -> list[Page]:
        """Load pages either from the cache or from Wikipedia, caching new entries along the way

        Handles batching the search; callers don't need to worry about that
        """
        # First, try to load page from cache
        cached_pages: list[Page] = compact([self.page_file_cache.get(pageid) for pageid in pageids])

        # Then, fetch page from Wikipedia for all pages we don't already have, and store back in cache for later use
        missing_pageids: set[int] = set(pageids) - set(page.id for page in cached_pages)

        CHUNK_SIZE = 1
        PARALLELISM = 20

        semaphore = asyncio.Semaphore(value=PARALLELISM)

        async def fetch_and_store(pageids: list[int]):
            async with semaphore:
                fetched_pages = await self.fetch_remote_pages(pageids)

            for fetched_page in fetched_pages:
                self.page_file_cache.store(fetched_page)

            print(f'Stored {len(fetched_pages)} pages')

            return fetched_pages

        coros = []

        for missing_pageid_chunk in chunk(list(missing_pageids), size=CHUNK_SIZE):
            coros.append(fetch_and_store(list(missing_pageid_chunk)))

        fetched_pages_results = await asyncio.gather(*coros)

        fetched_pages = [page for result in fetched_pages_results for page in result]

        # Finally, return in-order
        pages = cached_pages + fetched_pages

        pages_by_id = key_by(pages, lambda page: page.id)

        return [pages_by_id[pageid] for pageid in pageids]

    async def fetch_remote_pages(self, pageids: list[int], popular=False) -> list[Page]:
        """Fetches pages directly from Wikipedia, with no knowledge of the cache at all

        Limited to 50 pages; wikipedia will only fetch that many at once

        :param popular: If true, only fetch "links"; there are too many backlinks for these pages to fetch quickly
        """
        if not pageids:
            return []

        # Wikipedia API only supports 50 pageids at a time
        if len(pageids) > 50:
            raise Exception(f'Tried to fetch too many remote pages ({len(pageids)}); the limit is 50')

        print(f"Fetching {len(pageids)} pages")

        try:
            query_result = await self.wikipedia_api.query_simple(pageids=pageids, prop=['links', 'linkshere'] if not popular else ['links'])
        except PopularPageException as e:
            print('Got popular page exception!', e.pageids)
            normal_page_ids = list(set(pageids) - set(e.pageids))

            normal_pages = await self.fetch_remote_pages(normal_page_ids)
            large_pages = await self.fetch_remote_pages(e.pageids, popular=True)

            return normal_pages + large_pages

        pageids_by_link_name = {}
        pages: list[Page] = []

        for page_json in query_result.values():
            if 'missing' in page_json:
                continue

            page = Page(
                id=page_json["pageid"],
                name=page_json['title'],
                # Backlinks have page ID already loaded
                # Popular pages have too many page links to load, so we just avoid that entirely
                backlinks=[bl["pageid"] for bl in page_json["linkshere"]] if 'linkshere' in page_json else [],
                links=[],  # Links don't have page ID loaded, and need to be joined with "generator" results, below
                loaded=False
            )

            pages.append(page)

            for link in page_json["links"]:
                pageids_by_link_name[link["title"]] = page.id

        pages_by_id = key_by(pages, lambda page: page.id)

        # Retrieves a mix of all links for the pageids passed in
        generator_result = await self.wikipedia_api.query_links_generator(
            pageids=list(pages_by_id.keys()),
            prop='info',
        )

        for link_json in generator_result.values():
            if 'missing' in link_json:
                continue

            linked_from_page_id = pageids_by_link_name[link_json['title']]
            linked_from_page = pages_by_id[linked_from_page_id]

            linked_from_page.links.append(link_json['pageid'])

        for page in pages:
            # TODO: Figure out if this flag is needed
            page.loaded = True

        return pages

    async def load_pages_by_titles(self, titles: list[str]) -> list[Page]:
        results = await self.wikipedia_api.query_simple(titles=titles, prop=['info'])

        invalid_results = [result for result in results.values() if 'missing' in result]

        if invalid_results:
            raise Exception(f"The following titles are invalid: {", ".join(r["title"] for r in invalid_results)}")

        results_by_title = key_by(results.values(), lambda result: result["title"])

        return await self.load_pages(pageids=[results_by_title[title]["pageid"] for title in titles])
