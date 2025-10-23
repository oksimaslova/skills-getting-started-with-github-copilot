import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Programming Class" in data
    assert isinstance(data["Programming Class"], dict)

def test_signup_and_unregister():
    activity = "Programming Class"
    email = "pytestuser@mergington.edu"

    # Ensure not already registered
    client.post(f"/activities/{activity}/unregister?email={email}")

    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400

    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]

    # Unregister again should fail
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
