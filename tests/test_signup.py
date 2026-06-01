"""Tests for the POST /activities/{activity_name}/signup endpoint using AAA pattern."""


def test_signup_for_activity_success(client, sample_email, chess_club_activity):
    """Test successful signup for an activity."""
    # Arrange
    email = sample_email
    activity = chess_club_activity

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_signup_duplicate_email_returns_error(client, sample_email, chess_club_activity):
    """Test that signing up the same email twice returns a 400 error."""
    # Arrange
    email = sample_email
    activity = chess_club_activity
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_nonexistent_activity_returns_404(client, sample_email):
    """Test that signing up for a nonexistent activity returns 404."""
    # Arrange
    email = sample_email
    activity = "Nonexistent Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_adds_participant_to_activity(client, sample_email, chess_club_activity):
    """Test that signup actually adds the participant to the activity."""
    # Arrange
    email = sample_email
    activity = chess_club_activity

    # Act
    client.post(f"/activities/{activity}/signup", params={"email": email})
    response = client.get("/activities")

    # Assert
    data = response.json()
    assert email in data[activity]["participants"]


def test_signup_multiple_different_emails(client, chess_club_activity):
    """Test that multiple different emails can sign up for the same activity."""
    # Arrange
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    activity = chess_club_activity

    # Act
    response1 = client.post(f"/activities/{activity}/signup", params={"email": email1})
    response2 = client.post(f"/activities/{activity}/signup", params={"email": email2})

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    response = client.get("/activities")
    data = response.json()
    assert email1 in data[activity]["participants"]
    assert email2 in data[activity]["participants"]
