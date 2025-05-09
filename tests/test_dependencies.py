import pytest
from app.dependencies import (
    get_settings,
    get_email_service,
    get_current_user,
    require_role
)
from fastapi import HTTPException
from app.services.jwt_service import create_access_token


def test_get_settings_returns_settings_instance():
    settings = get_settings()
    assert settings is not None
    assert isinstance(settings.debug, bool)


def test_get_email_service_returns_instance():
    service = get_email_service()
    assert service is not None
    assert service.template_manager is not None


def test_get_current_user_valid_token(monkeypatch):
    token_data = {"sub": "testuser", "role": "ADMIN"}
    token = create_access_token(data=token_data)

    # Patch decode_token used inside get_current_user
    monkeypatch.setattr("app.dependencies.decode_token", lambda _: token_data)

    result = get_current_user(token)
    assert result["user_id"] == "testuser"
    assert result["role"] == "ADMIN"


def test_get_current_user_invalid_token(monkeypatch):
    monkeypatch.setattr("app.dependencies.decode_token", lambda _: None)

    with pytest.raises(HTTPException) as exc_info:
        get_current_user("invalidtoken")

    assert exc_info.value.status_code == 401


def test_require_role_allows_correct_role():
    current_user = {"user_id": "123", "role": "MANAGER"}
    checker = require_role("MANAGER")
    result = checker(current_user=current_user)
    assert result["role"] == "MANAGER"


def test_require_role_blocks_incorrect_role():
    current_user = {"user_id": "123", "role": "USER"}
    checker = require_role("ADMIN")

    with pytest.raises(HTTPException) as exc_info:
        checker(current_user=current_user)

    assert exc_info.value.status_code == 403
    assert "not permitted" in exc_info.value.detail
