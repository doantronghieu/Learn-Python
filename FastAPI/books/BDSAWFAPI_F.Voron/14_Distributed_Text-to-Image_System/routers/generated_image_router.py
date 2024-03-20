from pyexpat import model
from re import L
import add_packages
import contextlib

from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import image_generation_schema
from sql_toolkit import models, database
from workers import worker
from storages import minio
from storages.settings import settings

# *=============================================================================
router = APIRouter()

# *=============================================================================
async def get_generated_image_or_404(
    id: int, session: AsyncSession = Depends(database.get_async_session)
) -> models.GeneratedImage:
  query = select(models.GeneratedImage).where(models.GeneratedImage.id == id)
  result = await session.execute(query)
  image = result.scalar_one_or_none()

  if image is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

  return image

async def get_storage() -> minio.Storage:
  return minio.Storage()
# *=============================================================================
@router.post(
    "/", response_model=image_generation_schema.GeneratedImageRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_generated_image(
  generated_image_create: image_generation_schema.GeneratedImageCreate,
  session: AsyncSession = Depends(database.get_async_session),
) -> models.GeneratedImage:
  image = models.GeneratedImage(**generated_image_create.model_dump())
  session.add(image)
  await session.commit()

  # The worker read id from the database to retrieve the generation parameters.
  worker.task_text_to_image.send(image.id)

  return image

# *-----------------------------------------------------------------------------

@router.get(
  "/{id}", response_model=image_generation_schema.GeneratedImageRead,
)
async def get_generated_image(
  image: models.GeneratedImage = Depends(get_generated_image_or_404)
) -> models.GeneratedImage:
  return image

# *-----------------------------------------------------------------------------


@router.get("/{id}/url")
async def get_generated_image_url(
  image: models.GeneratedImage = Depends(get_generated_image_or_404),
  storage: minio.Storage = Depends(get_storage),
) -> image_generation_schema.GeneratedImageUrl:
  """Return pre-signed URL for GeneratedImage"""
  
  # check if the file_name property is set on the object
  if image.file_name is None:
    # the worker has not completed the task
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Image is not available yet. Please try again later."
    )
  
  url = storage.get_presigned_url(
    object_name=image.file_name, bucket_name=settings.storage_bucket,
  )
  
  return image_generation_schema.GeneratedImageUrl(url=url)
