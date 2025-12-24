import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_create_user_hand(client: AsyncClient):
    uri = "/metrics"
    response = await client.get(uri)
    assert response.status_code == 200
