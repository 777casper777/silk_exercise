from typing import Dict
from datetime import datetime
from app.models.unified_host import UnifiedHost


def normalize_qualys(raw_data: Dict) -> UnifiedHost:
    return UnifiedHost(
        id=str(raw_data.get("id")),
        hostname=raw_data.get("dnsHostName", "unknown"),
        ip_address=raw_data.get("address", "0.0.0.0"),
        os=raw_data.get("os"),
        vendor="qualys",
        last_seen=parse_datetime(
            raw_data.get("agentInfo", {}).get("lastCheckedIn", {}).get("$date")
        )
    )



def normalize_crowdstrike(raw_data: Dict) -> UnifiedHost:
    return UnifiedHost(
        id=str(raw_data.get("device_id")),
        hostname=raw_data.get("hostname", "unknown"),
        ip_address=raw_data.get("local_ip", "0.0.0.0"),
        os=raw_data.get("platform_name"),
        vendor="crowdstrike",
        last_seen=parse_datetime(
            raw_data.get("agent_local_time") or
            raw_data.get("modified_timestamp", {}).get("$date")
        )
    )


def parse_datetime(dt_str):
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except Exception:
        return None
