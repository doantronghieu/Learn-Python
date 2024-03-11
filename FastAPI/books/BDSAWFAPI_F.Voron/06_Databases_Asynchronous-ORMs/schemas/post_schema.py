import add_packages
from datetime import datetime
from typing import Union
from pydantic import BaseModel, Field
from schemas import comment_schema

class PostBase(BaseModel):
  title: str
  content: str
  # publication_date: datetime


  class Config:
    # Adds configuration options to Pydantic schemas
    # Make Pydantic work better with ORM
    # Properties accessed like an object using dot notation (o.title)
    # orm_mode = True
    from_attributes = True


class PostPartialUpdate(BaseModel):
  title: Union[str, None] = None
  content: Union[str, None] = None


class PostCreate(PostBase):
  # comments: list[comment_schema.CommentRead]
  pass


class PostRead(PostBase):
  id: int
  # Get comments of a post in a single request, serialization of post's comments.
  comments: list[comment_schema.CommentRead]
  
  class Config:
    from_attributes = True
