from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import logging

from app.database import Database
from app.dependencies import get_settings
from app.routers import user_routes  # Make sure this includes /auth/login
from app.utils.api_description import getDescription

# Initialize logger
logger = logging.getLogger(__name__)

app = FastAPI(
    title="User Management",
    description=getDescription(),
    version="0.0.1",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)

@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    Database.initialize(settings.database_url, settings.debug)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception occurred")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred."}
    )

# Ensure all routers including /auth/login are registered
app.include_router(user_routes.router)
