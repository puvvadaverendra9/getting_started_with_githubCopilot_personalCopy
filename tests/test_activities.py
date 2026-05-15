from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    """Test retrieving all activities"""
    # Arrange - No special setup needed
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    """Test successful signup for an activity"""
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]
    assert email in result["message"]

def test_signup_duplicate():
    """Test signing up twice fails"""
    # Arrange
    email = "dup@mergington.edu"
    activity = "Programming Class"
    client.post(f"/activities/{activity}/signup?email={email}")  # First signup
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]

def test_signup_invalid_activity():
    """Test signup for non-existent activity"""
    # Arrange
    email = "test@mergington.edu"
    invalid_activity = "NonExistent"
    
    # Act
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_unregister_success():
    """Test successful unregistration"""
    # Arrange
    email = "unreg@mergington.edu"
    activity = "Gym Class"
    client.post(f"/activities/{activity}/signup?email={email}")  # Signup first
    
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]

def test_unregister_not_signed_up():
    """Test unregistering a non-participant"""
    # Arrange
    email = "notsigned@mergington.edu"
    activity = "Gym Class"
    
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "not signed up" in result["detail"]

def test_unregister_invalid_activity():
    """Test unregister from non-existent activity"""
    # Arrange
    email = "test@mergington.edu"
    invalid_activity = "Invalid"
    
    # Act
    response = client.delete(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]