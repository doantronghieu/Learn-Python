from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader

router = APIRouter()



# Hardcoded Token compared to token passed in header to authorize endpoint
API_TOKEN = "SECRET_API_TOKEN"


@router.get("/protected-route")
async def protected_route(
  # Class Security dependency retrieves value from header using the name argument
  # Logic for checking header existence and value retrieval is included
  token: str = Depends(APIKeyHeader(name="Token")),
):
  if token != API_TOKEN:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
  return {
    "hello": "world",
  }