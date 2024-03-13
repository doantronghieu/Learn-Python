from fastapi import APIRouter, Depends, HTTPException, status, Response, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy import select, exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from schemas import user_schema

from sql_toolkit.database import get_async_session
from sql_toolkit.models import User

from utils import security_util, authen_util

from dependencies import auth_dep

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

@router.post("/login")
async def login(
  response: Response,
  email: str = Form(...),
  password: str = Form(...),
  session: AsyncSession = Depends(get_async_session),
):
  user = await authen_util.authenticate(email, password, session)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
  
  token = await authen_util.create_access_token(user, session)
  
  response.set_cookie(
    key="token",
    value=token.access_token,
    max_age=token.max_age(),
    # sent only over HTTPS and value can't be read from JavaScript
    secure=True,
    httponly=True,
    # control cookie sent in cross-origin context
    # allows cookie to be sent to subdomains but prevents for other sites
    samesite="lax",
  )
  
@router.get("/me", response_model=user_schema.UserRead)
async def get_me(user : User = Depends(auth_dep.get_current_user)):
  return user

@router.post("/me", response_model=user_schema.UserRead)
async def update_me(
  user_update: user_schema.UserUpdate,
  user: User = Depends(auth_dep.get_current_user),
  session: AsyncSession = Depends(get_async_session),
):
  user_update_dict = user_update.model_dump(exclude_unset=True)
  for key, value in user_update_dict.items():
    setattr(user, key, value)
    
  session.add(user)
  await session.commit()
  
  return user