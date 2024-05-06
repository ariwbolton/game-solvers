from typing import Iterable

from pydash import chunk, key_by, compact

from wikipedia_game_v2.page import Page
from wikipedia_game_v2.page_file_cache import PageFileCache
from wikipedia_game_v2.wikipedia_api import WikipediaAPI


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

        all_fetched_pages: list[Page] = []

        # TODO: Add concurrency

        for missing_pageid_chunk in chunk(list(missing_pageids), size=1):
            fetched_pages = await self.fetch_remote_pages(list(missing_pageid_chunk))

            for fetched_page in fetched_pages:
                self.page_file_cache.store(fetched_page)

            print(f'Stored {len(fetched_pages)} pages')

            all_fetched_pages.extend(fetched_pages)

        # Finally, return in-order
        pages = cached_pages + all_fetched_pages

        pages_by_id = key_by(pages, lambda page: page.id)

        return [pages_by_id[pageid] for pageid in pageids]

    async def fetch_remote_pages(self, pageids: list[int]) -> list[Page]:
        """Fetches pages directly from Wikipedia, with no knowledge of the cache at all

        Can handle a long list; uses concurrency
        """
        if not pageids:
            return []

        # Wikipedia API only supports 50 pageids at a time
        if len(pageids) > 50:
            raise Exception(f'Tried to fetch too many remote pages ({len(pageids)}); the limit is 50')

        # TODO: add concurrency

        print(f"Fetching {len(pageids)} pages")

        query_result = await self.wikipedia_api.query_simple(pageids=pageids, prop=['links', 'linkshere'])

        pageids_by_link_name = {}
        pages: list[Page] = []

        for page_json in query_result.values():
            if 'missing' in page_json:
                continue

            page = Page(
                id=page_json["pageid"],
                name=page_json['title'],
                backlinks=[bl["pageid"] for bl in page_json["linkshere"]],  # Backlinks have page ID already loaded
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
