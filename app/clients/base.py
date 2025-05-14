from typing import AsyncIterator

class BaseHostFetcher:
    async def fetch_hosts(self) -> AsyncIterator[dict]:
        """
        Asynchronously yields raw host data from a source.
        Each fetcher class (Qualys, Crowdstrike, etc.) must implement this method.
        """
        raise NotImplementedError("Subclasses must implement fetch_hosts")
