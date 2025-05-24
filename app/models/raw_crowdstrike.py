# 📝 This file contains a static sample of raw host data from the Crowdstrike API.
# It is NOT used in the main application logic.
# You can use this for local testing, normalization development, or debugging.
# Example usage: test how normalize_crowdstrike(data) handles this input.

from pydantic import BaseModel
from typing import Optional

class RawCrowdstrikeHost(BaseModel):
    device_id: str
    hostname: Optional[str]
    local_ip: str
    platform_name: Optional[str]
    last_seen: Optional[str]
    vendor: Optional[str] = "crowdstrike"