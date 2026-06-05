pytest_plugins = ["pytest_asyncio"]

import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from src.app import app


@pytest.fixture
async def async_client():
    """Provide an `httpx.AsyncClient` running the FastAPI app with lifespan managed.

    Yields an AsyncClient instance configured with the ASGI app so tests can call
    endpoints without a running server.
    """
    transport = ASGITransport(app=app)
    async with LifespanManager(app):
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            yield client
