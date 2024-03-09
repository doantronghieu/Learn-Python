from fastapi import FastAPI

from routers.posts import router as posts_router

app = FastAPI()

app.include_router(posts_router, prefix="/posts", tags=["posts"])

# uvicorn app:app --reload
