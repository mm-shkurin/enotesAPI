import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to eNotes.pro API"}

@pytest.mark.asyncio
async def test_vk_auth_redirect():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/auth/vk", follow_redirects=False)
        assert response.status_code == 307  # Redirect
        assert "oauth.vk.com" in response.headers["location"]

@pytest.mark.asyncio
async def test_vk_callback_without_code():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/auth/vk/callback")
        assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_me_endpoint_without_token():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/auth/me")
        assert response.status_code == 401
        assert "Token is required" in response.json()["detail"]

@pytest.mark.asyncio
async def test_me_endpoint_with_invalid_token():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/auth/me", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]

@pytest.mark.asyncio
async def test_test_auth_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/auth/test")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "vk_client_id" in data
        assert "redirect_uri" in data
