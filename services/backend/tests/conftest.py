from asgi_lifespan import LifespanManager

import pytest_asyncio
from httpx import AsyncClient, ASGITransport


from main import app


@pytest_asyncio.fixture(scope="session")
async def client():
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as ac:
            yield ac

