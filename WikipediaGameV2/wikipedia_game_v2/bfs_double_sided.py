from wikipedia_game_v2.bfs_inspectable import BFSInspectable
from wikipedia_game_v2.page import Page
from wikipedia_game_v2.page_loader import PageLoader


class BFSDoubleSided:
    def __init__(self, page_loader: PageLoader):
        self.page_loader = page_loader

    async def search(self, start: Page, end: Page) -> list[Page] | None:
        """Iterate forward from the start, AND backwards from the end, using the less costly side at each step"""
        if start.id == end.id:
            return [start]

        if end.id in start.links:
            return [start, end]

        forward = BFSInspectable(start=start, end=end, direction='forward', page_loader=self.page_loader)
        backward = BFSInspectable(start=end, end=start, direction='backward', page_loader=self.page_loader)

        step_count = 0
        forward_count = 0
        backward_count = 0

        while not (forward.current & backward.current) and forward.current and backward.current:
            step_count += 1

            print(f'Step {step_count}')
            print(f'Forward: {forward_count} steps, {len(forward.current)} nodes')
            print(f'Backward: {backward_count} steps, {len(backward.current)} nodes')

            if len(forward.current) <= len(backward.current):
                print('Stepping forwards...')
                forward_count += 1
                await forward.step()
            else:
                print('Stepping backwards...')
                backward_count += 1
                await backward.step()

            print('')

        if not forward.current or not backward.current:
            return None

        # We've found a path!
        overlap = forward.current & backward.current
        pivot = overlap.pop()

        path = forward.path(pivot)[:-1] + [pivot] + list(reversed(backward.path(pivot)[:-1]))

        return await self.page_loader.load_pages(pageids=path)
