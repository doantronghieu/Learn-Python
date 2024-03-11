import add_packages
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
  create_async_engine, AsyncSession, async_sessionmaker,
)
from sql.models import Base

DATABASE_URL = "postgresql+asyncpg://postgres:123456@127.0.0.1:5432/postgres"
# Object where SQLAlchemy will manage the connection with the database. 
# No connection is being made at this point
engine = create_async_engine(DATABASE_URL)
# Function to generate sessions tied to the database engine.
# Session establishes a connection with the database to store objects read from
# and written to the database, as a proxy between ORM concepts and SQL queries.
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
  # Dependency to yield a fresh session (a unit of work with the db).
  async with async_session_maker() as session:
    # Open a connection to db
    # `yield` keep session open until end of request
    yield session


async def create_all_tables():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)