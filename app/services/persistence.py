from motor.motor_asyncio import AsyncIOMotorClient
from app.models.unified_host import UnifiedHost
import os
import logging
from typing import List

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["host_db"]
collection = db["hosts"]


async def ensure_indexes():
    indexes = await collection.index_information()
    if "host_identity_idx" in indexes:
        await collection.drop_index("host_identity_idx")

    await collection.create_index(
        [("hostname", 1), ("ip_address", 1), ("vendor", 1)],
        name="host_identity_idx",
        unique=True
    )


async def upsert_host(host: UnifiedHost):
    query = {
        "hostname": host.hostname,
        "ip_address": host.ip_address,
        "vendor": host.vendor
    }
    update = {"$set": host.model_dump()}
    await collection.update_one(query, update, upsert=True)
    logging.info(f"Upserted host: {host.hostname} ({host.ip_address}) from {host.vendor}")

async def bulk_upsert_hosts(hosts: List[UnifiedHost]):
    logging.info(f"Upserting {len(hosts)} hosts...")
    for host in hosts:
        await upsert_host(host)
