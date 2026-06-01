"""Tests for the DELETE /activities/{activity_name}/participants endpoint using AAA pattern."""


def test_remove_participant_success(client, sample_email, chess_club_activity):
    """Test successful removal of a participant."""
    # Arrange
    email = sample_email
    activity = chess_club_activity
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]
    assert email in data["message"]


def test_remove_nonexistent_participant_returns_404(client, chess_club_activity):
    """Test that removing a nonexistent participant returns 404."""
    # Arrange
    email = "nonexistent@mergington.edu"
    activity = chess_club_activity

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]


def test_remove_participant_from_nonexistent_activity_returns_404(client, sample_email):
    """Test that removing a participant from a nonexistent activity returns 404."""
    # Arrange
    email = sample_email
    activity = "Nonexistent Club"

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_remove_deletes_participant_from_activity(client, sample_email, chess_club_activity):
    """Test that participant is actually removed from the activity."""
    # Arrange
    email = sample_email
    activity = chess_club_activity
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    client.delete(f"/activities/{activity}/participants", params={"email": email})
    response = client.get("/activities")

    # Assert
    data = response.json()
    assert email not in data[activity]["participants"]


def test_remove_allows_same_email_to_signup_again(client, sample_email, chess_club_activity):
    """Test that after removal, the same email can sign up again."""
    # Arrange
    email = sample_email
    activity = chess_club_activity
    client.post(f"/activities/{activity}/signup", params={"email": email})
    client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    get_response = client.get("/activities")
    data = get_response.json()
    assert email in data[activity]["participants"]
