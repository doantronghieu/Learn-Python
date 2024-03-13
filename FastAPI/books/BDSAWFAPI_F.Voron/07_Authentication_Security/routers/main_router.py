from fastapi import APIRouter, HTTPException, status, Depends

from schemas import user_schema
from dependencies import security_dep, auth_dep
from sql_toolkit.models import User

router = APIRouter()


@router.get("/csrf")
async def csrf():
    return None

@router.get("/protected-route", response_model=user_schema.UserRead)
async def protected_route(user: User = Depends(auth_dep.get_current_user)):
    return {
        user,
    }
