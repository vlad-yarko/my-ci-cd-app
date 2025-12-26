import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_health_endpoint(client: AsyncClient):
    uri = "/health"
    response = await client.get(uri)
    assert response.status_code == 200
