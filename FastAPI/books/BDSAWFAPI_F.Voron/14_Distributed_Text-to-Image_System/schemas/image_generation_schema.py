from datetime import datetime
from typing import Union
from pydantic import BaseModel, Field


class GeneratedImageBase(BaseModel):
  prompt: str
  negative_prompt: Union[str, None] = None
  num_steps: int = Field(50, gt=0, le=50)
  
  class Config:
    from_attributes = True


class GeneratedImageCreate(GeneratedImageBase):
  pass

class GeneratedImageRead(GeneratedImageBase):
  id: int
  created_at: datetime
  progress: int
  file_name: Union[str, None]

class GeneratedImageUrl(BaseModel):
  url: str