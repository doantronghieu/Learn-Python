import contextlib
from collections.abc import Sequence

from fastapi import FastAPI, Depends, HTTPException, Query, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import post_schema
from sql.database import create_all_tables, get_async_session

from routers import post_router, comment_router

# Creates the table’s schema in the database
# Creates schema on application start
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
  await create_all_tables()
  yield

app = FastAPI(lifespan=lifespan)

app.include_router(post_router.router, prefix="/posts", tags=["posts"])
app.include_router(comment_router.router, prefix="/posts", tags=["comments"])
