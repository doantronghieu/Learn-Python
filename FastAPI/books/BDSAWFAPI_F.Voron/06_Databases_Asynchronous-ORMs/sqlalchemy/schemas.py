import add_packages
from datetime import datetime
from typing import Union
from pydantic import BaseModel, Field

class PostBase(BaseModel):
  title: str
  content: str
  publication_date: datetime = Field(default_factory=datetime.now)
  
  class Config:
    # Adds configuration options to Pydantic schemas
    # Make Pydantic work better with ORM
    # Properties accessed like an object using dot notation (o.title)
    orm_mode = True
  
class PostPartialUpdate(BaseModel):
  title: Union[str, None] = None
  content: Union[str, None] = None

class PostCreate(PostBase):
  pass

class PostRead(PostBase):
  id: int