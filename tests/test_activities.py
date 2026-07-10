import pytest


@pytest.mark.asyncio
async def test_get_activities_returns_all_activities(async_client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = await async_client.get(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "Programming Class" in payload


@pytest.mark.asyncio
async def test_get_activities_contains_expected_fields(async_client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = await async_client.get(endpoint)
    payload = response.json()

    # Assert
    chess_club = payload["Chess Club"]
    assert response.status_code == 200
    assert set(chess_club.keys()) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }
    assert isinstance(chess_club["participants"], list)