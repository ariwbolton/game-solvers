from pydash import chunk, key_by

from wikipedia_game_v2.page import Page
from wikipedia_game_v2.wikipedia_api import WikipediaAPI


class PageFetcher:
    """TODO: Add caching so that this only needs to actually fetch pages we don't have already."""
    def __init__(self):
        self.wikipedia_api = WikipediaAPI()

    def get_pages(self, *, pageids: list[int]) -> list[Page]:
        # Wikipedia API only supports 50 at a time
        for pageid_chunk in chunk(pageids, size=50):
            query_result = self.wikipedia_api.query_simple(pageids=list(pageid_chunk), prop=['links', 'linkshere'])

            pages: list[Page] = []
            pageids_by_link_name = {}

            for page_json in query_result["query"]["pages"].values():
                if 'missing' in page_json:
                    continue

                page = Page(
                    id=page_json["pageid"],
                    name=page_json['title'],
                    backlinks=[bl["pageid"] for bl in page_json["linkshere"]],  # Backlinks have page ID already loaded
                    links=[],  # Links don't have page ID loaded, and need to bo joined with "generator" results, below
                    loaded=False
                )

                pages.append(page)

                for link in page_json["links"]:
                    pageids_by_link_name[link["title"]] = page.id


            pages_by_id = key_by(pages, lambda page: page.id)

            # Retrieves a mix of all links for the pageids passed in
            generator_result = self.wikipedia_api.query_generator(pageids=list(pageid_chunk), prop='info', generator='link')

            for link_json in generator_result["query"]["pages"].values():
                if 'missing' in link_json:
                    continue

                linked_from_page_id = pageids_by_link_name[link_json['title']]
                linked_from_page = pages_by_id[linked_from_page_id]

                linked_from_page.links.append(link_json['pageid'])

            for page in pages:
                # TODO: Figure out if this flag is needed
                page.loaded = True

            return pages




        return []
