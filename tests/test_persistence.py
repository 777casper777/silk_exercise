import pytest
from unittest.mock import AsyncMock, patch
from app.services.persistence import upsert_host
from app.models.unified_host import UnifiedHost
import datetime

@pytest.mark.asyncio
async def test_upsert_host():
    mock_collection = AsyncMock()
    mock_collection.update_one = AsyncMock()

    with patch("app.services.persistence.collection", mock_collection):
        host = UnifiedHost(
            id="x",
            hostname="t.local",
            ip_address="9.9.9.9",
            os="TestOS",
            vendor="test",
            last_seen=datetime.datetime.utcnow()
        )
        await upsert_host(host)
        mock_collection.update_one.assert_awaited_once()
