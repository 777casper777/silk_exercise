# 📝 This file contains a static sample of raw host data from the Qualys API.
# It is NOT used in the main application pipeline.
# It serves as a test fixture to verify normalization and data structure expectations.
# You can use this for debugging normalize_qualys(data) or creating unit tests.

from pydantic import BaseModel
from typing import Optional

class RawQualysHost(BaseModel):
    id: str
    dns: Optional[str]
    ip: str
    os: Optional[str]
    last_seen: Optional[str]
    vendor: Optional[str] = "qualys"