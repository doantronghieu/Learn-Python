from typing import Union
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sql_toolkit.models import User, AccessToken

from utils import security_util


async def authenticate(
    email: str, password: str, session: AsyncSession
) -> Union[User, None]:
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user: Union[User, None] = result.scalar_one_or_none()

    if user is None:
        return None

    if not security_util.verify_password(password, user.hashed_password):
        return None

    return user


async def create_access_token(
    user: User, session: AsyncSession
) -> AccessToken:
    access_token = AccessToken(user=user)
    session.add(access_token)
    await session.commit()
    return access_token

