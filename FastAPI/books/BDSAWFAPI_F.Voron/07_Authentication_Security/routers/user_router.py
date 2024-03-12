from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy import select, exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from schemas import user_schema

from sql_toolkit.database import get_async_session
from sql_toolkit.models import User

from utils import security_util, authen_util

router = APIRouter()

@router.post(
  "/register", status_code=status.HTTP_201_CREATED, 
  response_model=user_schema.UserRead,
)
async def register(
  user_create: user_schema.UserCreate, 
  session: AsyncSession = Depends(get_async_session)
) -> User:
  hashed_password = security_util.get_password_hash(user_create.password)
  user = User(
    **user_create.model_dump(exclude={"password"}),
    hashed_password=hashed_password,
  )
  
  try:
    session.add(user)
    await session.commit()
  except exc.IntegrityError:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Email already exists"
    )
  
  return user

@router.post("/token")
async def create_token(
  # automatically retrieve the access token and set the authorization header 
  # for subsequent requests
  form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
  session: AsyncSession = Depends(get_async_session),
):
  email = form_data.username
  password = form_data.password
  # retrieve a user
  user = await authen_util.authenticate(email, password, session)
  
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
  
  token = await authen_util.create_access_token(user, session)
  
  return {
    "access_token": token.access_token,
    "token_type": "bearer",
  }