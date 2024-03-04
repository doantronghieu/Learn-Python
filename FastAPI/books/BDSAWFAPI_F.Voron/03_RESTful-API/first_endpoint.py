# first_endpoint.py
from fastapi import FastAPI

app = FastAPI()

# Define a GET endpoint at the root path
# Always returning {"hello": "world"} JSON response.
@app.get("/")
async def hello_world():
  return {
    "hello": "world"
  }

"""
uvicorn first_endpoint:app
"""

# API expects integer in path. 
# Parameter name in path with curly braces. 
# specifying integer.
@app.get("/users/{id}")
# Same parameter defined as argument for path operation function with type hint
async def get_user_with_id(id: int):
  return {
    "id": id,
  }
  
@app.get("/users/{type}/{id}")
async def get_user_with_type_id(type: str, id: int):
  # The endpoint accepts any string as the type parameter.
  return {
    "type": type,
    "id": id,
  }