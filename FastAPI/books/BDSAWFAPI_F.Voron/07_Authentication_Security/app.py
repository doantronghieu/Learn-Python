import contextlib
import secrets
import os
from dotenv import dotenv_values

from fastapi import FastAPI, Request

from starlette.middleware.cors import CORSMiddleware
from starlette_csrf import CSRFMiddleware

from routers.main_router import router as main_router
from routers.user_router import router as users_router
from sql_toolkit.database import create_all_tables

env_vars = dotenv_values(".env")


@contextlib.asynccontextmanager
# Creates the table’s schema in the database
# Creates schema on application start
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    # catches preflight requests and returns response with CORS headers based
    # on configuration
    CORSMiddleware,
    # origins allowed to make requests to API
    allow_origins=["http://localhost:9000"],
    # Allow browsers send cookies cross-origin HTTP authenticated requests to API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # controls cache duration of CORS responses
    max_age=-1,
)

app.add_middleware(
    CSRFMiddleware,
    # strong passphrase for signing CSRF token
    secret=env_vars["CSRF_TOKEN_SECRET"],
    # cookie names triggering CSRF protection
    # Bypass CSRF check if no critical cookies
    sensitive_cookies={env_vars["TOKEN_COOKIE_NAME"]},
    # cross-origin retrieval of CSRF token cookie
    cookie_domain="localhost",
)

app.include_router(main_router, prefix="/main", tags=["main"])
app.include_router(users_router, prefix="/users", tags=["users"])
