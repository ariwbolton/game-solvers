import asyncio

import httpx

from wikipedia_game_v2.wikipedia_api import WikipediaAPI
from .bfs_double_sided import BFSDoubleSided
from .page_loader import PageLoader


def with_async_client(func):
    async def wrapper(*args, **kwargs):
        async with httpx.AsyncClient() as client:
            return await func(client, *args, **kwargs)

    return wrapper


@with_async_client
async def main(client: httpx.AsyncClient) -> None:
    wikipedia_api = WikipediaAPI(client)
    page_loader = PageLoader(wikipedia_api)
    bfs = BFSDoubleSided(page_loader=page_loader)

    stephen_curry_page_id = 5608488
    uranium_page_id = 31743

    start, end = await page_loader.load_pages(pageids=[stephen_curry_page_id, uranium_page_id])

    print('Starting search!', start.name, '->', end.name)

    path = await bfs.search(start, end)

    if path is None:
        print('No path found!')
    else:
        print(f'FOUND PATH!! Length {len(path)}')

        for page in path:
            print(page)


if __name__ == '__main__':
    asyncio.run(main())
