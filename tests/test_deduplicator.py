#LEGACY TEST — In-memory deduplication logic
import pytest
import datetime
from app.services.deduplicator import deduplicate_hosts
from app.models.unified_host import UnifiedHost

def test_deduplicate_hosts():
    now = datetime.datetime.utcnow()
    h1 = UnifiedHost(id="1", hostname="host1", ip_address="1.1.1.1", os="Linux", vendor="v1", last_seen=now)
    h2 = UnifiedHost(id="2", hostname="host1", ip_address="1.1.1.1", os="Windows", vendor="v2", last_seen=now - datetime.timedelta(days=1))
    h3 = UnifiedHost(id="3", hostname="host2", ip_address="2.2.2.2", os="Linux", vendor="v3", last_seen=now)

    result = deduplicate_hosts([h1, h2, h3])
    assert len(result) == 2
    assert any(h.id == "1" for h in result)
    assert any(h.id == "3" for h in result)

def test_deduplicate_prefers_latest():
    old = datetime.datetime(2024, 1, 1)
    new = datetime.datetime(2024, 5, 1)
    h1 = UnifiedHost(id="1", hostname="duplicate", ip_address="1.1.1.1", os="OldOS", vendor="old", last_seen=old)
    h2 = UnifiedHost(id="2", hostname="duplicate", ip_address="1.1.1.1", os="NewOS", vendor="new", last_seen=new)

    result = deduplicate_hosts([h1, h2])
    assert len(result) == 1
    assert result[0].id == "2"
