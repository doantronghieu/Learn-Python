import add_packages
from dependencies import secret_header
from fastapi import APIRouter, Depends

router = APIRouter(
  # dependencies=[Depends(secret_header.secret_header)] # option
)

@router.get("/route1")
async def router_route1():
  return {
    "route": "route1"
  }
  
@router.get("/route2")
async def router_route2():
  return {
    "route": "route2"
  }
