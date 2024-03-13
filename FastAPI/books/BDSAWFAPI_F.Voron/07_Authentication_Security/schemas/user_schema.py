from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
  email: EmailStr
  
  class Config:
    from_attributes = True

class UserCreate(UserBase):
  password: str

class UserUpdate(UserBase):
  pass

class User(UserBase):
  id: int
  hashed_password: str

class UserRead(UserBase):
  id: int