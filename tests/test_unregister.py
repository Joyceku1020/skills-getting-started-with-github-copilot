from urllib.parse import quote

import pytest

from src.app import activities


@pytest.mark.asyncio
async def test_unregister_success(async_client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{quote(activity_name, safe='')}/participants"

    # Act
    response = await async_client.delete(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


@pytest.mark.asyncio
async def test_unregister_fails_for_missing_activity(async_client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    endpoint = f"/activities/{quote(activity_name, safe='')}/participants"

    # Act
    response = await async_client.delete(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


@pytest.mark.asyncio
async def test_unregister_fails_for_non_enrolled_student(async_client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.enrolled@mergington.edu"
    endpoint = f"/activities/{quote(activity_name, safe='')}/participants"

    # Act
    response = await async_client.delete(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Student is not signed up for this activity"