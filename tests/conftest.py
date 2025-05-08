from builtins import range
from datetime import datetime
from uuid import uuid4
import smtplib
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from urllib.parse import urlencode
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session
from faker import Faker

from app.main import app
from app.database import Base, Database
from app.models.user_model import User, UserRole
from app.dependencies import get_db, get_settings
from app.utils.security import hash_password
from app.utils.template_manager import TemplateManager
from app.services.email_service import EmailService
from app.services.jwt_service import create_access_token
from app.services.user_service import UserService

fake = Faker()

settings = get_settings()
TEST_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(TEST_DATABASE_URL, echo=settings.debug)
AsyncTestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
AsyncSessionScoped = scoped_session(AsyncTestingSessionLocal)

@pytest.fixture
def mock_smtp(monkeypatch):
    class MockSMTP:
        def login(self, user, password): pass
        def sendmail(self, from_addr, to_addrs, msg): pass
        def starttls(self): pass
        def quit(self): pass
        def __enter__(self): return self
        def __exit__(self, exc_type, exc_val, exc_tb): pass

    def mock_connect(*args, **kwargs):
        return MockSMTP()

    monkeypatch.setattr(smtplib, "SMTP", mock_connect)

@pytest.fixture
def email_service():
    template_manager = TemplateManager()
    return EmailService(template_manager=template_manager)

@pytest.fixture(scope="function")
async def async_client(db_session):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        app.dependency_overrides[get_db] = lambda: db_session
        try:
            yield client
        finally:
            app.dependency_overrides.clear()

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    try:
        Database.initialize(settings.database_url)
    except Exception as e:
        pytest.fail(f"Failed to initialize the database: {str(e)}")

@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture(scope="function")
async def db_session(setup_database):
    async with AsyncSessionScoped() as session:
        try:
            yield session
        finally:
            await session.close()

# USER FIXTURES
@pytest.fixture(scope="function")
async def locked_user(db_session):
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": True,
        "failed_login_attempts": settings.max_login_attempts,
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def user(db_session):
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": False,
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def verified_user(db_session):
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": True,
        "is_locked": False,
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def unverified_user(db_session):
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": False,
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def users_with_same_role_50_users(db_session):
    users = []
    for _ in range(50):
        user_data = {
            "nickname": fake.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "hashed_password": hash_password("MySuperPassword$1234"),
            "role": UserRole.AUTHENTICATED,
            "email_verified": False,
            "is_locked": False,
        }
        user = User(**user_data)
        db_session.add(user)
        users.append(user)
    await db_session.commit()
    return users

# ADMIN & MANAGER
@pytest.fixture
async def admin_user(db_session: AsyncSession):
    user = User(
        nickname="admin_user",
        email="admin@example.com",
        first_name="John",
        last_name="Doe",
        hashed_password=hash_password("MySuperPassword$1234"),
        role=UserRole.ADMIN,
        is_locked=False,
        email_verified=True
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture
async def manager_user(db_session: AsyncSession):
    user = User(
        nickname="manager_john",
        first_name="John",
        last_name="Doe",
        email="manager_user@example.com",
        hashed_password=hash_password("MySuperPassword$1234"),
        role=UserRole.MANAGER,
        is_locked=False,
        email_verified=True
    )
    db_session.add(user)
    await db_session.commit()
    return user

# FORM DATA FIXTURES
@pytest.fixture
def user_base_data():
    return {
        "nickname": "testuser",
        "email": "john.doe@example.com",
        "full_name": "John Doe",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg"
    }

@pytest.fixture
def user_base_data_invalid():
    return {
        "nickname": "testuser",
        "email": "john.doe.example.com",
        "full_name": "John Doe",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg"
    }

@pytest.fixture
def user_create_data(user_base_data):
    return {**user_base_data, "password": "SecurePassword123!"}

@pytest.fixture
def user_update_data():
    return {
        "email": "john.doe.new@example.com",
        "full_name": "John H. Doe",
        "bio": "I specialize in backend development with Python and Node.js.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe_updated.jpg",
        "first_name": "John"
    }

@pytest.fixture
def user_response_data():
    return {
        "id": uuid4(),
        "nickname": "testuser",
        "email": "test@example.com",
        "last_login_at": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "links": []
    }

@pytest.fixture
def login_request_data():
    return {"email": "john.doe@example.com", "password": "SecurePassword123!"}

@pytest.fixture
async def user_token(async_client: AsyncClient, db_session: AsyncSession, email_service, mock_smtp):
    user_data = {
        "email": "user@example.com",
        "password": "UserStrong!123",
        "nickname": "usertest"
    }
    user = await UserService.create(db_session, user_data, email_service)
    user.email_verified = True
    await db_session.commit()

    form_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }

    login_response = await async_client.post(
        "/login/",
        data=urlencode(form_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    json_response = login_response.json()
    assert "access_token" in json_response, f"Missing access_token: {json_response}"
    return json_response["access_token"]

@pytest.fixture
async def admin_token(async_client: AsyncClient, admin_user, email_service, mock_smtp):
    form_data = {
        "username": admin_user.email,
        "password": "MySuperPassword$1234"
    }

    login_response = await async_client.post(
        "/login/",
        data=urlencode(form_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    json_response = login_response.json()
    assert "access_token" in json_response, f"Missing access_token: {json_response}"
    return json_response["access_token"]

@pytest.fixture
async def manager_token(async_client: AsyncClient, manager_user, email_service, mock_smtp):
    form_data = {
        "username": manager_user.email,
        "password": "MySuperPassword$1234"
    }

    login_response = await async_client.post(
        "/login/",
        data=urlencode(form_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    json_response = login_response.json()
    assert "access_token" in json_response, f"Missing access_token: {json_response}"
    return json_response["access_token"]
