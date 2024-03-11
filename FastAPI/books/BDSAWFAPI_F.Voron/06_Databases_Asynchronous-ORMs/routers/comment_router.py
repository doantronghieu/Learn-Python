import add_packages
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from schemas import comment_schema
from sql.models import Post, Comment
from sql.database import get_async_session
from dependencies import post_dep

router = APIRouter()

@router.post(
  "/{id}/comments",
  response_model=comment_schema.CommentRead,
  status_code=status.HTTP_201_CREATED,
)
async def create_comment(
  comment_create: comment_schema.CommentCreate,
  # Check the existence of the post
  post: Post = Depends(post_dep.get_post_or_404),
  session: AsyncSession = Depends(get_async_session),
) -> Comment:
  # `relationship` allows direct assignment of post object on comment object
  # ORM will set right value in post_id column.
  comment = Comment(**comment_create.model_dump(), post=post)
  session.add(comment)
  await session.commit()
  return comment


@router.get(
    "/{id}/comments",
    response_model=list[comment_schema.CommentRead],
)
async def get_comments_by_post(
    post: Post = Depends(post_dep.get_post_or_404),
    session: AsyncSession = Depends(get_async_session),
) -> list[comment_schema.CommentRead]:
    # Use options to eagerly load the post's comments
    query = select(Post).filter_by(
        id=post.id).options(selectinload(Post.comments))
    result = await session.execute(query)

    # Get the post with comments from the executed query result
    post_with_comments = result.scalar()

    # If the post exists, return its comments
    if post_with_comments:
        return post_with_comments.comments

    # If the post doesn't exist, return an empty list
    return []
