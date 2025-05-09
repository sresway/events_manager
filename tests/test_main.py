import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import logging

logger = logging.getLogger("test")

@pytest.mark.asyncio
async def test_app_exception_handler():
    # Create a local FastAPI app instance with an error route
    test_app = FastAPI()

    @test_app.get("/force-error")
    async def force_error():
        raise Exception("Boom")

    @test_app.exception_handler(Exception)
    async def custom_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception occurred in test app")
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An unexpected error occurred."}
        )

    # Use ASGITransport to allow catching exceptions
    transport = ASGITransport(app=test_app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        response = await ac.get("/force-error")

    assert response.status_code == 500
    assert response.json()["message"] == "An unexpected error occurred."


@pytest.mark.asyncio
async def test_app_root_route_exists():
    from app.main import app as base_app  # Imported here to avoid startup conflicts
    async with AsyncClient(app=base_app, base_url="http://testserver") as ac:
        response = await ac.get("/docs")
    assert response.status_code == 200
