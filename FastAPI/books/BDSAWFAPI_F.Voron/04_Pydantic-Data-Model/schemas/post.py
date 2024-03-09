import add_packages
from pydantic import BaseModel
from typing import Union

class PostBase(BaseModel):
  title: str
  content: str
  
  def excerpt(self) -> str:
    return f"{self.content[:140]}..."

class PostCreate(PostBase):
  # For a POST endpoint to create a new post. 
  # User provides title and content; ID determined by database.
  
  # API for creates endpoints. Receive PostCreate instance with title and content.
  # Need to build Post instance before storing in database
  
  # Use the dict method and the unpacking syntax.
  pass

class PostRead(PostBase):
  # For retrieving post data. Includes title, content, and associated ID in database.
  id: int

class Post(PostBase):
  # Carries all data for database storage. 
  # Includes number of views kept secret for internal statistics.
  id: int
  nb_view: int = 0
  
class PostPartialUpdate(BaseModel):
  title: Union[str, None] = None
  content: Union[str, None] = None