from pydantic import BaseModel
from typing import Optional

class RawCrowdstrikeHost(BaseModel):
    device_id: str
    hostname: Optional[str]
    local_ip: str
    platform_name: Optional[str]
    last_seen: Optional[str]
    vendor: Optional[str] = "crowdstrike"