from settings.config import settings

def test_settings_defaults():
    assert settings.max_login_attempts == 3
    assert str(settings.server_base_url) == "http://localhost/"
    assert settings.secret_key == "secret-key"
    assert settings.jwt_algorithm == "HS256"
    assert settings.access_token_expire_minutes == 15
    assert settings.refresh_token_expire_minutes == 1440
    assert settings.database_url.startswith("postgresql+asyncpg")
    assert settings.smtp_port == 2525
    assert isinstance(settings.send_real_mail, bool)
