import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Fixture that resets activities to initial state before each test."""
    # Store original state
    original_participants = {
        activity: list(details["participants"]) for activity, details in activities.items()
    }

    yield  # Run the test

    # Restore original state after the test
    for activity, details in activities.items():
        details["participants"] = original_participants.get(activity, [])


@pytest.fixture
def client():
    """Fixture providing a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Fixture providing a sample email for testing."""
    return "test@mergington.edu"


@pytest.fixture
def chess_club_activity():
    """Fixture providing a sample activity name."""
    return "Chess Club"
