from typing import Optional, List, Dict
from uuid import UUID, uuid1
from enum import Enum
from pydantic import BaseModel
from datetime import date, datetime
import schema_user

#*=============================================================================

class PostType(str, Enum):
  information = "information"
  inquiry = "inquiry"
  quote = "quote"
  twit = "twit"

class ForumPost(BaseModel):
  id: UUID
  topic: Optional[str] = None
  message: str
  post_type: PostType
  date_posted: datetime
  username: str

class ForumDiscussion(BaseModel):
  id: UUID
  main_post: ForumPost
  replies: Optional[List[ForumPost]] = None
  author: schema_user.UserProfile