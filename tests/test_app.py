import pytest


class TestGetActivities:
    """Test GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: client is initialized with fresh activities
        Act: GET /activities
        Assert: response contains all activities with correct structure
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Art Studio" in activities
        assert len(activities) == 3
    
    def test_get_activities_returns_correct_structure(self, client):
        """
        Arrange: client is initialized with fresh activities
        Act: GET /activities
        Assert: each activity has required fields
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)


class TestSignupForActivity:
    """Test POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client):
        """
        Arrange: Art Studio has 0 participants (max 1)
        Act: POST signup for Art Studio
        Assert: student is added and message returned
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Art Studio"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity}"
        
        # Verify participant was added
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity]["participants"]
    
    def test_signup_duplicate_email_fails(self, client):
        """
        Arrange: michael@mergington.edu already signed up for Chess Club
        Act: POST signup with same email for same activity
        Assert: returns 400 error
        """
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is already signed up for this activity"
    
    def test_signup_activity_full_fails(self, client):
        """
        Arrange: Programming Class is at max capacity (2/2)
        Act: POST signup to Programming Class
        Assert: returns 400 with capacity error
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Programming Class"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Activity is at maximum capacity"
    
    def test_signup_nonexistent_activity_fails(self, client):
        """
        Arrange: "Nonexistent Club" does not exist
        Act: POST signup to nonexistent activity
        Assert: returns 404 error
        """
        # Arrange
        email = "student@mergington.edu"
        activity = "Nonexistent Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestUnregisterFromActivity:
    """Test DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client):
        """
        Arrange: michael@mergington.edu is in Chess Club participants
        Act: DELETE unregister from Chess Club
        Assert: student is removed and message returned
        """
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {email} from {activity}"
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        assert email not in activities_response.json()[activity]["participants"]
    
    def test_unregister_not_registered_fails(self, client):
        """
        Arrange: newstudent@mergington.edu is not in Chess Club
        Act: DELETE unregister from Chess Club
        Assert: returns 400 error
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is not signed up for this activity"
    
    def test_unregister_nonexistent_activity_fails(self, client):
        """
        Arrange: "Nonexistent Club" does not exist
        Act: DELETE unregister from nonexistent activity
        Assert: returns 404 error
        """
        # Arrange
        email = "student@mergington.edu"
        activity = "Nonexistent Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestRootRedirect:
    """Test GET / endpoint"""
    
    def test_root_redirects_to_index(self, client):
        """
        Arrange: client is initialized
        Act: GET /
        Assert: redirects to /static/index.html
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
