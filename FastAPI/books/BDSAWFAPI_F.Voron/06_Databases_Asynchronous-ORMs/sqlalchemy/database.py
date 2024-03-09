import add_packages
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
  create_async_engine, AsyncSession, async_sessionmaker,
)

DATABASE_URL = "postgresql+asyncpg://postgres:123456@127.0.0.1:5432/postgres"
# Object where SQLAlchemy will manage the connection with the database. 
# No connection is being made at this point
engine = create_async_engine(DATABASE_URL)
# Function to generate sessions tied to the database engine.
# Session establishes a connection with the database to store objects read from
# and written to the database, as a proxy between ORM concepts and SQL queries.
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

