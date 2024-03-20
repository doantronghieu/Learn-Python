import add_packages
from fastapi import APIRouter
import dramatiq
from workers.worker import task_roll_dice
#*=============================================================================
router = APIRouter()

#*=============================================================================
@router.get("/")
async def hello():
  return {
    "hello": "world",
  }

#*-----------------------------------------------------------------------------


@router.get("/roll")
async def roll():
  return {
    "result": task_roll_dice()
  }

#*-----------------------------------------------------------------------------

if __name__ == "__main__":
  task_roll_dice.send()