import add_packages
from fastapi import APIRouter, HTTPException, status
from schemas.post import PostCreate, PostPartialUpdate, PostRead, Post
import db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=PostRead)
# response_model argument is set on the path operation decorator. 
# Prompts FastAPI to build a JSON response with only the fields of PostRead, 
# even though a Post instance is returned at the end of the function.
async def create_post(post_create: PostCreate):
  new_id = max(db.posts.keys() or (0,)) + 1
  # TransformPostCreate object into a Post object.
  # Use the dict method and the unpacking syntax.
  # Assign missing fields using keyword arguments
  # Unpack the dictionary representation of post_create.
  # "**" transforms a dictionary into keyword arguments. 
  post = Post(id=new_id, **post_create.model_dump())
  db.posts[new_id] = post
  return post

@router.patch("/{id}", response_model=PostRead)
# Accept a subset of Post fields. 
async def partial_update(id: int, post_update: PostPartialUpdate):
  try:
    # Retrieve an existing post by ID. 
    post = db.posts[id]
    post_data = Post(**post)  # Instantiate a Post object from the dictionary
    
    # Update only the fields in the payload and keep others untouched. 
    # Transforming PostPartialUpdate into a dictionary 
    # Clones a Pydantic object into another instance 
    # `update` expects a dictionary with fields to be updated during copying
    updated_post = post_data.model_copy(
        update=post_update.model_dump(exclude_unset=True))
    db.posts[updated_post.id] = updated_post
    return updated_post
  except KeyError:
    raise HTTPException(status.HTTP_404_NOT_FOUND)