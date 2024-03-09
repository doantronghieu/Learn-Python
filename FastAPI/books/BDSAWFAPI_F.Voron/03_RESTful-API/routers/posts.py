import add_packages

from fastapi import APIRouter, Response, status

from schemas.post import Post, PublicPost

from db import posts

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    return post


@router.get("/{id}", response_model=PublicPost)
# nb_views property no longer present. response_model option converts Post
# instance to PublicPost instance before serialization, keeping private data safe.
async def get_post(id: int):
    return posts[id]


@router.put("/{id}")
async def update_or_create_post(
    id: int, post: Post, response: Response
):
    # Check if the ID in the path exists in the database.
    # If not, change the status code to 201.
    if id not in posts:
        response.status_code = status.HTTP_201_CREATED

    # Assign the post to this ID in the database.
    posts[id] = post

    return posts[id]
