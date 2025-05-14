from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UnifiedHost(BaseModel):
    id: str = Field(..., description="Unique identifier of the host")
    hostname: str = Field(..., description="Hostname or name of the host")
    ip_address: str = Field(..., description="Primary IP address")
    os: Optional[str] = Field(None, description="Operating system name")
    vendor: str = Field(..., description="Vendor that reported this host, e.g., 'qualys'")
    last_seen: Optional[datetime] = Field(None, description="Timestamp when the host was last seen")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "host-123",
                "hostname": "host1.local",
                "ip_address": "192.168.1.10",
                "os": "Linux",
                "vendor": "qualys",
                "last_seen": "2024-05-10T10:00:00Z"
            }
        }
    )
