import pytest
import jwt
from datetime import timedelta, datetime
from app.services.jwt_service import create_access_token, decode_token
from settings.config import settings

def test_create_and_decode_valid_token():
    data = {"sub": "user_id_123", "role": "authenticated"}
    token = create_access_token(data=data)
    
    decoded = decode_token(token)
    
    assert decoded is not None
    assert decoded["sub"] == "user_id_123"
    assert decoded["role"] == "AUTHENTICATED"  # should be uppercased
    assert "exp" in decoded

def test_decode_invalid_token():
    invalid_token = "this.is.not.a.valid.token"
    result = decode_token(invalid_token)
    assert result is None

def test_decode_expired_token():
    data = {"sub": "user_id_456", "role": "authenticated"}
    expired_token = create_access_token(
        data=data, 
        expires_delta=timedelta(seconds=-1)  # already expired
    )

    result = decode_token(expired_token)
    assert result is None

def test_token_contains_expiry():
    data = {"sub": "test_user", "role": "authenticated"}
    token = create_access_token(data=data)
    decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm], options={"verify_exp": False})
    
    assert "exp" in decoded
    assert isinstance(decoded["exp"], int)
    assert datetime.utcfromtimestamp(decoded["exp"]) > datetime.utcnow()
