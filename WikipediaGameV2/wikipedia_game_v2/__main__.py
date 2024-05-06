
from .bfs_double_sided import BFSDoubleSided
from .page_loader import PageLoader

def run():
    page_loader = PageLoader()
    bfs = BFSDoubleSided(page_loader=page_loader)

    stephen_curry_page_id = 5608488
    uranium_page_id = 31743

    start, end = page_loader.load_pages(pageids=[stephen_curry_page_id, uranium_page_id])

    print('Starting search!', start.name, ' -> ', end.name)

    path = bfs.search(start, end)

    if path is None:
        print('No path found!')
    else:
        print(path)



if __name__ == '__main__':
    run()