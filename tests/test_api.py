import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to eNotes.pro API"}

def test_vk_auth_redirect():
    response = client.get("/auth/vk")
    assert response.status_code == 307  # Redirect
    assert "oauth.vk.com" in response.headers["location"]

def test_vk_callback_without_code():
    response = client.get("/auth/vk/callback")
    assert response.status_code == 422  # Validation error

def test_me_endpoint_without_token():
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert "Token is required" in response.json()["detail"]

def test_me_endpoint_with_invalid_token():
    response = client.get("/auth/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]
