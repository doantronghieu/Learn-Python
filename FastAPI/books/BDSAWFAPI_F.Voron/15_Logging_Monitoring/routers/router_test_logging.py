import add_packages
from fastapi import APIRouter, Depends

from my_logging.logger import logger
from dependencies import dep_auth_sec
#*=============================================================================
router = APIRouter()

#*=============================================================================
@router.post("/is-even", dependencies=[Depends(dep_auth_sec.secret_header)])
async def is_even(n: int) -> bool:
  logger_context = logger.bind(n=n)
  logger_context.debug("Check if even")
  if not isinstance(n, int):
    logger_context.error("Not an integer")
    raise TypeError()
  return n % 2 == 0

