from builtins import str
import pytest
from httpx import AsyncClient
from app.main import app
from app.models.user_model import User
from app.utils.nickname_gen import generate_nickname
from app.utils.security import hash_password
from app.services.jwt_service import decode_token
from urllib.parse import urlencode

# ----------------------------------------------
# Test user creation restrictions
# ----------------------------------------------
@pytest.mark.asyncio
async def test_create_user_access_denied(async_client, user_token, email_service, mock_smtp):
    headers = {"Authorization": f"Bearer {user_token}"}
    user_data = {
        "nickname": generate_nickname(),
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    response = await async_client.post("/users/", json=user_data, headers=headers)
    assert response.status_code == 403

# ----------------------------------------------
# Test user profile upgrade to professional
# ----------------------------------------------
@pytest.mark.asyncio
async def test_upgrade_user_to_professional_success(async_client, admin_user, user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post(f"/users/{user.id}/upgrade", headers=headers)
    assert response.status_code == 200
    assert response.json()["is_professional"] is True

@pytest.mark.asyncio
async def test_upgrade_user_to_professional_forbidden(async_client, user_token, admin_user):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.post(f"/users/{admin_user.id}/upgrade", headers=headers)
    assert response.status_code == 403 or response.status_code == 401
