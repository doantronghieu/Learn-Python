import add_packages
from fastapi import FastAPI
from routers import router_users, router_discussions

#*=============================================================================
# Instantiate FastAPI class to be used later as a Python @app decorator, which
# provides application with some features such as routes, middleware, 
# exception handlers, and path operations.
app = FastAPI()

app.include_router(
  router_users.router, prefix="/users", tags=["users"]
)
app.include_router(
  router_discussions.router, prefix="/discussions", tags=["discussions"]
)

#*=============================================================================
@app.get("/index")
async def index():
  # The GET API service method returns a JSON object.
  return {
    "message": "Welcome FastAPI Nerds",
  }

