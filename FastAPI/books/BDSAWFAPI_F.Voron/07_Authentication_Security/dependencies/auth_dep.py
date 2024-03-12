from datetime import datetime, timezone
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sql_toolkit.database import get_async_session
from sql_toolkit.models import User, AccessToken

async def get_current_user(
  # Checks for the access token in the Authorization header and informs the 
  # OpenAPI schema that the endpoint to get a fresh token is tokenUrl.
  token: str = Depends(OAuth2PasswordBearer(tokenUrl="/users/token")),
  session: AsyncSession = Depends(get_async_session)
) -> User:
  # Match token and ensure expiration date is in the future
  query = select(AccessToken).where(
    AccessToken.access_token == token,
    AccessToken.expiration_date >= datetime.now(tz=timezone.utc)
  )
  result = await session.execute(query)
  access_token: Union[AccessToken, None] = result.scalar_one_or_none()
  
  if access_token is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
  
  return access_token.user  