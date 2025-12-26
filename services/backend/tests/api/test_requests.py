import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_get_requests(client: AsyncClient):
    uri = "/requests"
    response = await client.get(uri)
    assert response.status_code == 200
