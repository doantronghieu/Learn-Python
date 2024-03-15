import add_packages
from collections.abc import Sequence
from fastapi import APIRouter, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from schemas import post_schema
from sql.models import Post
from sql.database import get_async_session
from dependencies import pagination_dep, post_dep

router = APIRouter()


# *-----------------------------------------------------------------------------


@router.post(
    "/", response_model=post_schema.PostRead, status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post_create: post_schema.PostCreate,
    # Inject fresh SQLAlchemy session
    session: AsyncSession = Depends(get_async_session)
) -> Post:

    # Transform Pydantic schema into SQLAlchemy model, save in database
    post = Post(**post_create.model_dump())

    # Add the post to the sesion memory, not in the database yet
    session.add(post)
    
    # Tell the session to generate the appropriate SQL queries
    # Perform an I/O operation on the database
    # Always call commit after write operation, changes must be written in database.
    await session.commit()
    await session.refresh(post)
    
    # Ensure the comments are loaded along with the posts
    query = select(Post).options(selectinload(Post.comments)).where(Post.id == post.id)
    result = await session.execute(query)
    post = result.scalar_one_or_none()
    
    # FastAPI transform ORM object to response_model orm_mode enabled Pydantic schema.
    return post


@router.get("/", response_model=list[post_schema.PostRead])
async def list_posts(
    paginatiton: tuple[int, int] = Depends(pagination_dep.pagination),
    session: AsyncSession = Depends(get_async_session),
) -> Sequence[post_schema.PostRead]:
    skip, limit = paginatiton

    # Build a query, pass model class to choose table
    query = select(Post).offset(skip).limit(
        limit).options(selectinload(Post.comments))

    # Execute query asyncly of fresh session object injected by dependency.
    result = await session.execute(query)

    # Result ORM object is an instance of the Result class of SQLAlchemy representing
    # the results of the SQL query.
    # `scalars` returns actual Post objects, `all` returns them as a sequence.
    posts = result.scalars().all()
    
    # Convert SQLAlchemy Post objects to Pydantic PostRead objects
    # post_reads = [post_schema.PostRead.model_validate(post) for post in posts]

    return posts


@router.get("/{id}", response_model=post_schema.PostRead)
async def get_post(
    post: Post = Depends(post_dep.get_post_or_404)
) -> Post:
    return post


@router.patch("/{id}", response_model=post_schema.PostRead)
async def update_post(
    post_update: post_schema.PostPartialUpdate,
    post: Post = Depends(post_dep.get_post_or_404),
    session: AsyncSession = Depends(get_async_session),
) -> Post:
    post_update_dict = post_update.model_dump(exclude_unset=True)
    for key, value in post_update_dict.items():
        # Operate directly on the post entiry to modify it.
        setattr(post, key, value)
        
    # Save it in the session and commit it to the database.
    session.add(post)
    await session.commit()

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: Post = Depends(post_dep.get_post_or_404),
    session: AsyncSession = Depends(get_async_session),
):
    await session.delete(post)
    await session.commit()
