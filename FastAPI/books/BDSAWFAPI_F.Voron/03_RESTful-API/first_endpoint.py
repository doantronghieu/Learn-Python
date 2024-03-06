# first_endpoint.py
from enum import Enum
from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel
#*-----------------------------------------------------------------------------

# Define string enumeration by inheriting from str type and Enum class.
class UserType(str, Enum):
  # List allowed values as class properties: property name and string value.
  STANDARD = "standard"
  ADMIN = "admin"
  
class UsersFormat(str, Enum):
  SHORT = "short"
  FULL = "full"
  
class User(BaseModel):
  name: str
  age: int

class Company(BaseModel):
  name: str
#*-----------------------------------------------------------------------------

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
async def get_user_with_id(id: int = Path(..., ge=1)):
  # Value of Path is default value for the id argument
  # Ellipsis syntax indicates no default value is expected, parameter is required
  return {
    "id": id,
  }
  
@app.get("/users/{type}/{id}")
async def get_user_with_type_id(type: UserType, id: int):
  # Type hint type argument with enum class.
  # The endpoint accepts any string as the type parameter.
  return {
    "type": type,
    "id": id,
  }

# Path parameter for French license plates in the form of AB-123-CD with a 
# length of 9 characters.
@app.get("/license-plates/{license}")
async def get_license_plate(
  # license plate number validation using regular expression (prefixed with r)
  # ensures exact match of license plate format
  license: str = Path(..., regex=r"^\w{2}-\d{3}-\w{2}%"),
):
  return {
    "license": license,
  }

@app.get("/users")
# Declare query parameters as arguments of path operation function. 
# If not in path pattern, FastAPI considers them as query parameters.
async def get_user(
  format: UsersFormat, 
  # Force page greater than 0 and size less than or equal to 100.
  page: int = Query(1, gt=0), # Default 1
  size: int = Query(10, lt=100),
):
  # Omitting the format parameter in the URL results in a 422 error response.
  # UsersFormat enumeration limits the allowed values for this parameter
  return {
    "page": page,
    "size": size,
    "format": format,
  }

@app.post("/users")
# argument `user` for path operation function with User class as type hint.
# FastAPI understands `user` data in request payload.
# Access user object instance's properties using dot notation (user.name).
async def create_user(user: User):
  return {
    # FastAPI automatically converts the object into JSON for the HTTP response.
    user
  }