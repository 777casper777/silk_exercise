import asyncio
import os
import logging
from celery import Celery
from redis.asyncio import Redis
from redis.exceptions import RedisError
from app.config import ACTIVE_FETCHERS
from app.loader import load_fetchers
from app.services.normalizer import normalize_qualys, normalize_crowdstrike
from app.services.persistence import upsert_host
from app.models.unified_host import UnifiedHost

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
USE_TTL = os.getenv("USE_REDIS_TTL", "true").lower() == "true"
DEDUP_TTL = int(os.getenv("DEDUP_TTL", 60 * 60 * 24))  # default: 1 day

app = Celery("tasks", broker=REDIS_URL)

@app.task
def run_pipeline():
    asyncio.run(_run_async_pipeline())


async def _run_async_pipeline():
    fetchers = load_fetchers()
    redis = Redis.from_url(REDIS_URL)
    await redis.ping()
    logger.info("✅ Redis connected")

    total_processed = 0
    total_inserted = 0
    total_skipped = 0
    total_redis_hits = 0
    total_redis_misses = 0

    for fetcher in fetchers:
        logger.info(f"📡 Fetching from: {fetcher.__class__.__name__}")
        async for raw in fetcher.fetch_hosts():
            vendor = raw.get("source") or raw.get("vendor")
            if vendor == "qualys":
                host = normalize_qualys(raw)
            elif vendor == "crowdstrike":
                host = normalize_crowdstrike(raw)
            else:
                continue

            key = f"dedup:{vendor}:{host.hostname}:{host.ip_address}"

            if await redis.exists(key):
                total_skipped += 1
                total_redis_hits += 1
                continue

            total_redis_misses += 1
            if USE_TTL:
                await redis.set(key, 1, ex=DEDUP_TTL)
            else:
                await redis.set(key, 1)

            await upsert_host(host)

            total_processed += 1
            total_inserted += 1

            if total_processed % 1000 == 0:
                logger.info(
                    f"⏱ Processed: {total_processed}, Inserted: {total_inserted}, Skipped (duplicates): {total_skipped}"
                )

    logger.info("✅ Pipeline completed")
    logger.info(f"🔢 Total processed: {total_processed}")
    logger.info(f"✅ Inserted into Mongo: {total_inserted}")
    logger.info(f"🚫 Skipped (duplicates): {total_skipped}")
    logger.info(f"💡 Redis hits: {total_redis_hits}, Redis misses: {total_redis_misses}")

    await redis.close()
