import add_packages
from fastapi import HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sql.models import Post
from sql.database import get_async_session

async def get_post_or_404(
    id: int, session: AsyncSession = Depends(get_async_session),
) -> Post:
    # Build select query, retrieve only the post matching the desired ID
    # Tells ORM to automatically retrieve associated comments of the post when
    # performing the query
    # Set column to compare
    query = select(Post)\
                .options(selectinload(Post.comments))\
                .where(Post.id == id)
    # Asynchronous ORM controls queries
    # Allows loading everything in single or few queries
    # Performs eager loading on relationships directly from the ORM object.
    result = await session.execute(query)
    
    # Tells SQLAlchemy to return a single object if it exists, or None otherwise
    post = result.scalar_one_or_none()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return post

