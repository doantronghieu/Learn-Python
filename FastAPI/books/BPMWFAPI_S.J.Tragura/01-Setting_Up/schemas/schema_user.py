import add_packages
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID, uuid1
from enum import Enum

#*=============================================================================
class User(BaseModel):
  username: str
  password: str

class ValidUser(BaseModel):
  id: UUID
  username: str
  password: str
  passphrase: str

#*-----------------------------------------------------------------------------
class UserType(str, Enum):
  admin = "admin"
  teacher = "teacher"
  alumni = "alumni"
  student = "student"

class UserProfile(BaseModel):
  firstname: str
  lastname: str
  middle_initial: str
  age: Optional[int] = 0
  salary: Optional[int] = 0
  birthday: date
  user_type: UserType

#*-----------------------------------------------------------------------------
class Post(BaseModel):
  topic: Optional[str] = None
  message: str
  date_posted: datetime

#*-----------------------------------------------------------------------------
