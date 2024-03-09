from fastapi import Depends, FastAPI
from dependencies import secret_header
from routers.users import router as users_router
from routers.items import router as items_router
from routers.posts import router as posts_router
from routers.secret import router as secret_router

app = FastAPI(
  # Execute logging or rate-limiting functionality for every API endpoint with 
  # dependencies
  # dependencies=[Depends(secret_header.secret_header)] # option
)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(items_router, prefix="/items", tags=["items"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(secret_router, prefix="/secret", tags=["secret"],
                   dependencies=[Depends(secret_header.secret_header)]
                   )
# uvicorn app:app --reload