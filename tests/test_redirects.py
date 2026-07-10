import pytest


@pytest.mark.asyncio
async def test_root_redirects_to_static_index(async_client):
    # Arrange
    endpoint = "/"

    # Act
    response = await async_client.get(endpoint, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"