# first_endpoint.py
from enum import Enum
from fastapi import (
    Body, Cookie, FastAPI, File, Form, Header, Path, Query, Request, Response,
    status, UploadFile
)
from pydantic import BaseModel
from typing import Union

# *-----------------------------------------------------------------------------

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
    # Pydantic model with a single string name property.
    name: str


class Post(BaseModel):
    title: str
    # The nb_views property is in the output. We don’t want this.
    nb_views: int


class PublicPost(BaseModel):
    title: str
# *-----------------------------------------------------------------------------


# Dummy DB
posts = {
    1: Post(title="Hello", nb_views=100)
}
# *-----------------------------------------------------------------------------

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


@app.get("/headers")
async def custom_header(response: Response):
    # The Response object provides access to properties, including headers. \
    # It is a dictionary with the header name as the key and its value.
    response.headers["Custom-Header"] = "Custom-Header-Value"

    # Don’t have to return the Response object. Can still return JSON-encodable
    # data, FastAPI will take care of forming a proper response, including the
    # headers. The response_model and status_code options are still honored.
    return {
        "hello": "world"
    }


@app.get("/headers/hello")
async def get_header_hello(
    hello: str = Header(...),
):
    # Use the Header function as a default value for the hello argument.
    # The name of the argument determines the key of the header to retrieve.
    # FastAPI retrieved the header value without a default value specified,
    # making the header required.
    # If missing, a 422 status error response will be returned.
    return {
        "hello": hello,
    }


@app.get("/headers/user-agent")
async def get_header_user_agent(
    # FastAPI automatically converts header names into lowercase and snake case,
    # making it compatible with any valid Python variable name.
    # User agent is an HTTP header added automatically by most HTTP clients and
    # web browsers to identify the application making the request.
    # Web servers use this information to adapt the response.
    user_agent: str = Header(...),
):
    return {
        "user_agent": user_agent,
    }


@app.get("/cookies")
async def custom_cookie(response: Response):
    # Set a cookie named cookie-name with the value of cookie-value.
    # Valid for 86,400 seconds before the browser removes it.
    # Call the method multiple times to set several cookies.
    response.set_cookie("cookie-name", "cookie-value", max_age=86400)
    return {
        "hello": "world",
    }


@app.get("/users")
# Declare query parameters as arguments of path operation function.
# If not in path pattern, FastAPI considers them as query parameters.
async def get_user(
    format: UsersFormat,
    # Force page greater than 0 and size less than or equal to 100.
    page: int = Query(1, gt=0),  # Default 1
    size: int = Query(10, lt=100),
):
    # Omitting the format parameter in the URL results in a 422 error response.
    # UsersFormat enumeration limits the allowed values for this parameter
    return {
        "page": page,
        "size": size,
        "format": format,
    }


@app.get("/users/{id}")
# API expects integer in path.
# Parameter name in path with curly braces.
# specifying integer.
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


@app.post("/users")
# argument `user` for path operation function with User class as type hint.
# FastAPI understands `user` data in request payload.
# Access user object instance's properties using dot notation (user.name).
async def create_user(
    user: User,
    company: Company,
    # Singular body values for a single property not part of any model.
    # integer between 1 and 3
    priority: int = Body(..., ge=1, le=3),
):
    return {
        # FastAPI automatically converts the object into JSON for the HTTP response.
        "user": user,
        "company": company,
        "priority": priority,
    }


@app.get("/license-plates/{license}")
# Path parameter for French license plates in the form of AB-123-CD with a
# length of 9 characters.
async def get_license_plate(
    # license plate number validation using regular expression (prefixed with r)
    # ensures exact match of license plate format
    license: str = Path(..., regex=r"^\w{2}-\d{3}-\w{2}%"),
):
    return {
        "license": license,
    }


@app.post('/blogs')
# The Content-Type header and body data representation have changed in the request.
# The response in JSON. FastAPI always output a JSON response
async def create_blog(
    # FastAPI does not allow defining Pydantic models for form data validation.
    # Fields must be manually defined as arguments for the path operation function.
    title: str = Form(...),
    page: int = Form(...),
):
    return {
        "title": title,
        "page": page,
    }


@app.post("/files")
async def upload_file(file: UploadFile = File(...)):
    # UploadFile class stores data in memory up to a threshold and then
    # automatically store it on disk.
    # The class exposes metadata like content type and a file-like interface for
    # manipulation
    return {
        "file_name": file.filename,
        "content_type": file.content_type,
    }


@app.post("/files_multiple")
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    return [
        {
            "file_name": file.filename, "content_type": file.content_type,
        }
        for file in files
    ]


@app.get("/cookies")
async def get_cookie(
    # Set default value None to Cookie function. Proceed without generating
    # 422 status error response if cookie not set in request.
    hello: Union[str, None] = Cookie(None)
):
    return {
        "hello": hello,
    }


@app.get("/requests")
async def get_request_object(request: Request):
    return {
        "path": request.url.path,
    }


@app.get("/posts/{id}", response_model=PublicPost)
# nb_views property no longer present. response_model option converts Post
# instance to PublicPost instance before serialization, keeping private data safe.
async def get_post(id: int):
    return posts[id]


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    return post

@app.put("/posts/{id}")
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