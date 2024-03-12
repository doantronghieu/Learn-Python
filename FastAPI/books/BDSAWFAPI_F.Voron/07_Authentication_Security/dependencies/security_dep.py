from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

async def api_token(
  # Class Security dependency retrieves value from header using the name argument
  # Logic for checking header existence and value retrieval is included
  token: str = Depends(APIKeyHeader(name="Token")),
):
  # Hardcoded Token compared to token passed in header to authorize endpoint
  if token != "SECRET_API_TOKEN":
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

