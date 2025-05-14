import pytest
from app.services.normalizer import normalize_qualys, normalize_crowdstrike
from app.models.unified_host import UnifiedHost


def test_normalize_qualys():
    raw = {
        "id": "123",
        "dns": "host1.qualys.local",
        "ip": "192.168.1.1",
        "os": "Ubuntu",
        "last_seen": "2024-05-10T12:00:00Z",
        "vendor": "qualys"
    }
    host = normalize_qualys(raw)
    assert isinstance(host, UnifiedHost)
    assert host.hostname == "host1.qualys.local"
    assert host.ip_address == "192.168.1.1"
    assert host.vendor == "qualys"


def test_normalize_crowdstrike():
    raw = {
        "device_id": "abc",
        "hostname": "crowd1.local",
        "local_ip": "10.0.0.1",
        "platform_name": "Windows",
        "last_seen": "2024-05-09T18:30:00Z",
        "vendor": "crowdstrike"
    }
    host = normalize_crowdstrike(raw)
    assert isinstance(host, UnifiedHost)
    assert host.hostname == "crowd1.local"
    assert host.ip_address == "10.0.0.1"
    assert host.vendor == "crowdstrike"
