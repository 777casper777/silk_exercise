from typing import AsyncIterator, Callable

async def paginated_fetch(fetch_fn: Callable[[int, int], AsyncIterator[dict]], batch_size: int = 2) -> AsyncIterator[dict]:
    skip = 0
    while True:
        found = False
        async for item in fetch_fn(skip, batch_size):
            found = True
            yield item
        if not found:
            break
        skip += batch_size
