from typing import Union
from fastapi import HTTPException, Header, status

def secret_header(secret_header: Union[str, None] = Header(None)) -> None:
  # Dependency checks for a header named Secret-Header in the request.
  # If it's missing or not equal to SECRET_VALUE, a 403 error will be raised.
  if not secret_header or secret_header != "SECRET_VALUE":
    raise HTTPException(status.HTTP_403_FORBIDDEN)