from pydantic import BaseModel
from typing import Optional

class RawQualysHost(BaseModel):
    id: str
    dns: Optional[str]
    ip: str
    os: Optional[str]
    last_seen: Optional[str]
    vendor: Optional[str] = "qualys"