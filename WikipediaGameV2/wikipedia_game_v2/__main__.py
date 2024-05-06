
from .bfs_double_sided import BFSDoubleSided
from .page_loader import PageLoader
from .graph import Graph

def run():
    page_loader = PageLoader()
    graph = Graph(page_loader=page_loader)
    bfs = BFSDoubleSided(graph=graph)

    stephen_curry_page_id = 5608488
    uranium_page_id = 31743

    start, end = page_loader.load_pages(pageids=[stephen_curry_page_id, uranium_page_id])

    print('loaded pages!', start, end)

    return

    path = bfs.search(start, end)

    if path is None:
        print('No path found!')
    else:
        print(path)



if __name__ == '__main__':
    run()