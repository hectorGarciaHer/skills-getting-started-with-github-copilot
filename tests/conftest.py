import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


@pytest.fixture
def client():
    """
    Provide a TestClient with fresh app state for each test.
    This prevents test pollution by resetting activities before each test.
    """
    # Save original activities
    original_activities = copy.deepcopy(activities)
    
    # Reset activities to a clean test state
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 2,  # Small capacity for testing limits
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media techniques",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 1,  # Very small for testing capacity
            "participants": []
        }
    })
    
    yield TestClient(app)
    
    # Cleanup: restore original activities after test
    activities.clear()
    activities.update(original_activities)
