import add_packages
from uuid import UUID
from fastapi import APIRouter

from db.db_dummy import db
#*=============================================================================

router = APIRouter()

#*=============================================================================

@router.delete("/posts/remove/{username}")
def delete_discussion(username: str, id: UUID):
  user = db["valid_users"].get(username)
  discussion = db["discussion_posts"].get(id)
  
  if user is None:
    return {
      "message": "user does not exist."
    }
  if discussion is None:
    return {
      "message": "post does not exist."
    }
  
  del db["discussion_posts"][id]
  return {
    "message": "main post deleted."
  }
