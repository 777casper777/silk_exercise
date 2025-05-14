import pytest
import datetime
import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.unified_host import UnifiedHost
from app.services.persistence import upsert_host

# Use environment variables for configuration (Docker compatible)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
TEST_DB_NAME = os.getenv("DB_NAME", "testdb")
TEST_COLLECTION_NAME = "hosts"

@pytest.mark.asyncio
async def test_upsert_host_real_db():
    # Connect to MongoDB using Motor client
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[TEST_DB_NAME]
    collection = db[TEST_COLLECTION_NAME]

    # Override the collection in the persistence module
    from app.services import persistence
    persistence.collection = collection

    # Sample host document
    host = UnifiedHost(
        id="test-id-123",
        hostname="test-host.local",
        ip_address="10.1.1.1",
        os="TestLinux",
        vendor="test-vendor",
        last_seen=datetime.datetime.utcnow()
    )

    # Perform an upsert operation
    await upsert_host(host)

    # Query back the inserted document
    result = await collection.find_one({"id": "test-id-123"})
    print("Inserted document:", result)  # Debug output

    # Assertions
    assert result is not None
    assert result["hostname"] == "test-host.local"

    # Cleanup
    #await collection.delete_one({"id": "test-id-123"})
    client.close()
