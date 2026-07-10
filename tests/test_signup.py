from urllib.parse import quote

import pytest

from src.app import activities


@pytest.mark.asyncio
async def test_signup_success(async_client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    endpoint = f"/activities/{quote(activity_name, safe='')}/signup"

    # Act
    response = await async_client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


@pytest.mark.asyncio
async def test_signup_fails_for_missing_activity(async_client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    endpoint = f"/activities/{quote(activity_name, safe='')}/signup"

    # Act
    response = await async_client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


@pytest.mark.asyncio
async def test_signup_fails_for_duplicate_student(async_client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{quote(activity_name, safe='')}/signup"

    # Act
    response = await async_client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


@pytest.mark.asyncio
async def test_signup_fails_when_activity_is_full(async_client):
    # Arrange
    activity_name = "Chess Club"
    email = "capacity.test@mergington.edu"
    activities[activity_name]["max_participants"] = len(activities[activity_name]["participants"])
    endpoint = f"/activities/{quote(activity_name, safe='')}/signup"

    # Act
    response = await async_client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Activity is full"