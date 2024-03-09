# app.py
from enum import Enum
from fastapi import (
    Body, Cookie, FastAPI, File, Form, HTTPException, Header, Path, Query, 
    Request, Response, status, UploadFile
)
from fastapi.responses import (
    FileResponse, HTMLResponse, PlainTextResponse, RedirectResponse
)
import pathlib
from pydantic import BaseModel
from typing import Union

from routers.posts import router as posts_router
from routers.users import router as users_router

# *-----------------------------------------------------------------------------

app = FastAPI()

app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(users_router, prefix="/users", tags=["users"])

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


@app.post("/password")
async def check_password(
    password: str = Body(...),
    password_confirm: str = Body(...),
):
    if password != password_confirm:
        # Raise a 400 Bad Request error if the password and password_ confirm
        # payload properties don’t match.
        # Error message wrapped in a JSON object with detail key.
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Passwords don't match.",
                "hints": [
                    "Check the caps lock on your keyboard.",
                    ("Try to make the password visible by clicking on the eye "
                     "icon to check your typing.")
                ]
            }
        )
    return {
        "message": "Passwords match."
    }


@app.get("/html", response_class=HTMLResponse)
# By setting response_class argument on decorator, change class used by FastAPI
# to build response.
async def get_html():
    # Return valid data for this response.
    return """
        <html>
            <head>
                <title>Hello world!</title>
            </head>
            <body>
                <h1>Hello world!</h1>
            </body>
        </html>
        """


@app.get("/text", response_class=PlainTextResponse)
async def text():
    return "Hello World!"


@app.get("/redirect")
async def redirect():
    return RedirectResponse(
        "http://google.com/", status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )


@app.get("/cat")
async def get_cat():
    root_directory = pathlib.Path(__file__).parent.parent
    picture_path = root_directory / "assets" / "cat.jpg"
    return FileResponse(picture_path)


@app.get("/xml")
# Return an XML response.
async def get_xml():
    content = """<?xml version="1.0" encoding="UTF-8"?>
        <Hello>World</Hello>
    """
    return Response(content=content, media_type="application/xml")
