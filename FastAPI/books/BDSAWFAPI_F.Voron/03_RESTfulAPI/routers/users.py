import add_packages
from fastapi import APIRouter, Body, HTTPException, Path, Query, status

import db
from schemas.user import UserType, User, Company, UsersFormat

# Instead of instantiating the FastAPI class, instantiate the APIRouter class. 
# Use it to decorate path operation functions.
router = APIRouter()

@router.get("/")
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


@router.post("/")
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
    
@router.get("/all")
async def get_all() -> list[User]:
    return list(db.users.values())

@router.get("/{id}")
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


@router.get("/{type}/{id}")
async def get_user_with_type_id(type: UserType, id: int):
    # Type hint type argument with enum class.
    # The endpoint accepts any string as the type parameter.
    return {
        "type": type,
        "id": id,
    }



