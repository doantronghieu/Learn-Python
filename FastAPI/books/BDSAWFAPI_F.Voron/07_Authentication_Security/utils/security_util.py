import add_packages
import secrets
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
  """Compare password hashes"""
  return pwd_context.verify(plain_password, hashed_password)


def get_expiration_date(duration_seconds: int = 86400) -> datetime:
    return datetime.now(tz=timezone.utc) + timedelta(seconds=duration_seconds)


def generate_token() -> str:
    """generates random secure passphrase"""
    return secrets.token_urlsafe(32)
