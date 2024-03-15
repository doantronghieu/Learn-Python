from datetime import datetime
from pydantic import BaseModel, Field

class CommentBase(BaseModel):
  # publication_date: datetime = Field(default_factory=datetime.now)
  content: str
  
  class Config:
    from_attributes = True

class CommentCreate(CommentBase):
  pass

class CommentRead(CommentBase):
  id: int
  post_id: int