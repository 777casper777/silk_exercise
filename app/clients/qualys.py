import os
import httpx
from app.clients.base import BaseHostFetcher
from app.utils.pagination import paginated_fetch

QUALYS_API_URL = "https://api.recruiting.app.silk.security/api/qualys/hosts/get"
TOKEN = os.getenv("API_TOKEN")

class QualysFetcher(BaseHostFetcher):
    async def fetch_hosts(self):
        async for host in paginated_fetch(self._fetch_page, batch_size=2):
            yield host

    async def _fetch_page(self, skip: int, limit: int):
        if limit > 2:
            limit = 2  # API constraint safeguard

        print(f"[Qualys] Fetching: skip={skip}, limit={limit}")

        async with httpx.AsyncClient() as client:
            params = {"skip": skip, "limit": limit}
            headers = {
                "accept": "application/json",
                "token": TOKEN
            }
            response = await client.post(QUALYS_API_URL, params=params, headers=headers, json={})
            if response.status_code != 200:
                print(f"[Qualys] Error {response.status_code}")
                print(f"[Qualys] Raw response text: {response.text}")
                try:
                    print(f"[Qualys] Parsed JSON error: {response.json()}")
                except Exception as e:
                    print(f"[Qualys] Failed to parse JSON: {e}")
                return
            data = response.json()
            for host in data:
                host["vendor"] = "qualys"
                yield host
