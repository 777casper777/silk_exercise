# Legacy deduplication logic (deprecated)
# Replaced by Redis-based global deduplication in fetch_and_process.py

from typing import List
from app.models.unified_host import UnifiedHost

def deduplicate_hosts(hosts: List[UnifiedHost]) -> List[UnifiedHost]:
    unique = {}
    for host in hosts:
        key = (host.hostname, host.ip_address)
        existing = unique.get(key)
        if not existing:
            unique[key] = host
        else:
            # merge logic: prefer latest last_seen
            if (host.last_seen and (not existing.last_seen or host.last_seen > existing.last_seen)):
                unique[key] = host
    return list(unique.values())
