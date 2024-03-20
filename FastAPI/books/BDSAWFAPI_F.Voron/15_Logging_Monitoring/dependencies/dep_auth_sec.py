from typing import Union
from fastapi import Header, HTTPException, status

from my_logging.logger import logger

def secret_header(secret_header: Union[str, None] = Header(None)) -> None:
  logger.debug("Check secret header")
  if not secret_header or secret_header != "123456":
    logger.warning("Invalid of missing secret header")
    raise HTTPException(status.HTTP_403_FORBIDDEN)
  