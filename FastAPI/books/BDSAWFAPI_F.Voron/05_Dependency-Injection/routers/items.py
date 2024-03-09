import add_packages
from typing import Any
from fastapi import APIRouter, Depends, Query
from dependencies import pagination, secret_header

router = APIRouter()

# Could pull from configuration file or environment variable.
custom_pagination = pagination.Pagination(maximum_limit=50)

@router.get("/")
async def list_items(
  p: tuple[int, int] = Depends(custom_pagination), # class __call__ method
  # p: tuple[int, int] = Depends(custom_pagination.skip_limit), # class custom method
):
  # Uses pagination dependency.
  # FastAPI handles arguments on dependency and matches with request data.
  # Define resulting argument name, use function result as default value
  # `Depends` executes Dependency function when endpoint is called
  # `Depends` function requires manually type hinting dependency result
  skip, limit = p
  # The query parameters have been retrieved thanks to the function dependency.
  # Calling the endpoint without the query parameter will return the default values.
  return {
    "skip": skip,
    "limit": limit,
  }

# Can add dependency on path operation decorator instead of arguments.
# The path operation decorator accepts dependencies argument. 
# Wrap function with the Depends function.
@router.get("/protected-route", dependencies=[Depends(secret_header.secret_header)])
async def protected_route():
  return {
    "hello": "world"
  }