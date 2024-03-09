from fastapi import APIRouter, Header

router = APIRouter()

@router.get("/")
async def header(user_agent: str = Header(...)):
  # Header function automatically gets request object, retrieves header,
  # returns value, or raises error if not present. 
  # From developer’s perspective, don’t know how handled required objects for 
  # operation: just ask for needed value. Dependency injection.
  return {
    "user_agent": user_agent
  }