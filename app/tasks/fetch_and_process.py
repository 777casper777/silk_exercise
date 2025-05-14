import asyncio
from celery import Celery
from app.config import ACTIVE_FETCHERS
from app.loader import load_fetchers
from app.services.normalizer import normalize_qualys, normalize_crowdstrike
from app.services.deduplicator import deduplicate_hosts
from app.services.persistence import bulk_upsert_hosts
import os

app = Celery("tasks", broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"))

@app.task
def run_pipeline():
    asyncio.run(_run_async_pipeline())


async def _run_async_pipeline():
    fetchers = load_fetchers()
    raw_hosts = []


    for fetcher in fetchers:
       async for host in fetcher.fetch_hosts():
          raw_hosts.append(host)


    normalized = []
    for raw in raw_hosts:
        vendor = raw.get("source") or raw.get("vendor")
        if vendor == "qualys":
            normalized.append(normalize_qualys(raw))
        elif vendor == "crowdstrike":
            normalized.append(normalize_crowdstrike(raw))

    deduped = deduplicate_hosts(normalized)
    #deduped = {}
    await bulk_upsert_hosts(deduped)