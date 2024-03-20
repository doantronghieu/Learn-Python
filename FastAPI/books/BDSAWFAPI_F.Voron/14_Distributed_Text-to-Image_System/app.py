import add_packages
from fastapi import FastAPI, status
import dramatiq

from schemas import image_generation_schema
from workers import worker
from routers import generated_image_router

#*=============================================================================
app = FastAPI()

app.include_router(
  generated_image_router, prefix="/generated-images", tags=["generated-images"],
)

#*=============================================================================