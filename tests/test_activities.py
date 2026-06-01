"""Tests for the GET /activities endpoint using AAA (Arrange-Act-Assert) pattern."""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities."""
    # Arrange: no setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_has_required_fields(client):
    """Test that each activity has required fields."""
    # Arrange: no setup needed

    # Act
    response = client.get("/activities")

    # Assert
    data = response.json()
    for activity_name, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)


def test_get_activities_returns_json(client):
    """Test that GET /activities returns valid JSON."""
    # Arrange: no setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
