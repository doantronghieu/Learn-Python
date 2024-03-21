import add_packages
from typing import Optional, Dict, List
from uuid import UUID
from fastapi import APIRouter
from bcrypt import hashpw, gensalt, checkpw

from schemas import schema_user
from db.db_dummy import db

#*=============================================================================
router = APIRouter()


#*=============================================================================
@router.get("/login")
# Query parameters
async def login(username: str, password: str):
  if db["valid_users"].get(username) == None:
    return {
      "message": "user does not exist."
    }
  
  user = db["valid_users"].get(username)
  if checkpw(password.encode(), user.passphrase.encode()):
    return user
  else:
    return {
      "message": "invalid user."
    }

@router.post("/login/signup")
async def signup(username: str, password: str):
  if username is None or password is None:
    return {
      "message": "invalid user."
    }
  elif db["valid_users"].get(username) is not None:
    return {
      "message": "user exist."
    }
  else:
    user = schema_user.User(username=username, password=password)
    db["pending_users"][username] = user
    return user

@router.get("/login/{username}/{password}")
# Multiple path parameters. Ensure leftmost path parameters are more likely to
# be filled with values than rightmost ones
async def login_with_token(username: str, password: str, id: UUID):
  user = db["valid_users"].get(username)
  
  if user is None:
    return {
      "message": "user does not exist."
    }
  
  if user.id == id and checkpw(password.encode(), user.passphrase):
    return user
  
  return {
    "message": "invalid user."
  }

@router.delete("/login/remove/{username}")
async def delete_user(username: str):
  if username is None:
    return {
      "message": "invalid user"
    }
  
  del db["valid_users"][username]

  return {
    "message": "user deleted."
  }

@router.delete("/login/remove/all")
async def delete_users(usernames: List[str]):
  for user in usernames:
    del db["valid_users"][user]

  return {
    "message": "users deleted."
  }

@router.delete("/delete/users/pending")
# TODO

@router.put("/account/profile/update/{username}")
# Path parameters. Declared with type hints after setting them in the URL.
async def update_profile(
  username: str, id: UUID, new_profile: schema_user.UserProfile,
):
  user = db["valid_users"].get(username)

  if user is None:
    return {
      "message": "user does not exist."
    }
  
  if user.id == id:
    db["valid_profile"][username] = new_profile
    return {
      "message": "successfully updated."
    }
  
@router.patch("/account/profile/update/names/{username}")
def update_profile_names(
  id: UUID, username: str = "", new_names: Optional[Dict[str, str]] = None,
):
  user = db["valid_users"].get(username)
  
  if user is None or user.id != id:
    return {
      "message": "user does not exits."
    }
  elif new_names is None:
    return {
      "message": "new names are required."
    }
  
  profile = db["valid_profile"][username]
  profile.firstname = new_names["firstname"]
  profile.lastname = new_names["lastname"]
  profile.middle_initial = new_names["middle_initial"]
  db["valid_profile"] = profile
  
  return {
    "message": "successfully updated."
  }


