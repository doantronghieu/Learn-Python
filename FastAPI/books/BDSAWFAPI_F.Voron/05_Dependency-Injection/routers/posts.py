import add_packages
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.post import Post, PostPartialUpdate
import db

router = APIRouter()

async def get_post_or_404(id: int) -> Post:
  # Dependency definition
  # Takes in ID (pulled from the corresponding path parameter) of the post we 
  # want to retrieve. Check whether it exists in database, if not, 
  # raise an HTTP exception with a 404 status code.
  try:
    return db.posts[id]
  # Errors can be raised in dependencies.
  except KeyError:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.get("/{id}")
# Remember to include the ID parameter in the path of the endpoints.
async def get_post(post: Post = Depends(get_post_or_404)):
  return post

@router.patch("/{id}")
async def update_post(
  post_update: PostPartialUpdate,
  post: Post = Depends(get_post_or_404)
):
  post_data = Post(**post)  # Instantiate a Post object from the dictionary
  updated_post = post_data.model_copy(update=post_update.model_dump())
  db.posts[updated_post.id] = updated_post
  return updated_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post: Post = Depends(get_post_or_404)):
  db.posts.pop(post.id)