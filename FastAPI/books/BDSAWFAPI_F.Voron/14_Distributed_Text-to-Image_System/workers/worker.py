import add_packages
import uuid
import asyncio
from typing import Union
from PIL import Image
from sqlalchemy import select

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.middleware import Middleware

from models.text_to_image import TextToImage
from sql_toolkit import models, database
from storages import minio
from storages.settings import settings

#*=============================================================================
class TextToImageMiddleware(Middleware):
  def __init__(self) -> None:
    super().__init__()
    self.text_to_image = TextToImage()
  
  def after_process_boot(self, broker):
    self.text_to_image.load_model()
    return super().after_process_boot(broker)

middleware_text_to_image = TextToImageMiddleware()
broker_redis = RedisBroker(host="localhost")
broker_redis.add_middleware(middleware_text_to_image)
dramatiq.set_broker(broker_redis)

#*=============================================================================
def get_image(id: int) -> models.GeneratedImage:
  """
  Retrieve GeneratedImage from database using ID from task argument.
  
  Dramatiq doesn't support running async functions directly, must manually 
  schedule their execution with asyncio.run
  """
  async def _get_image(id: int) -> models.GeneratedImage:
    async with database.async_session_maker() as session:
      query = select(models.GeneratedImage).where(models.GeneratedImage.id == id)
      result = await session.execute(query)
      image = result.scalar_one_or_none()
      
      if image is None:
        raise Exception("Image does not exist.")
      
      return image
  
  # Running an async function and returning result for synchronous calling in task
  return asyncio.run(_get_image(id))

def update_progress(image: models.GeneratedImage, step: int):
  async def _update_progress(image: models.GeneratedImage, step: int):
    async with database.async_session_maker() as session:
      image.progress = int((step/image.num_steps)*100)
      session.add(image)
      await session.commit()
  
  asyncio.run(_update_progress(image, step))

def update_file_name(image: models.GeneratedImage, file_name: str):
  """Save random filename in database to retrieve file for user"""
  async def _update_file_name(image: models.GeneratedImage, file_name: str):
    async with database.async_session_maker() as session:
      image.file_name = file_name
      session.add(image)
      await session.commit()

  asyncio.run(_update_file_name(image, file_name))

@dramatiq.actor()
def task_text_to_image(image_id: int):
  """
  Read and write GeneratedImage data to synchronize between the API server and worker.
  """
  
  image = get_image(image_id)
  
  def callback(step: int, _timestep, _tensor):
    """Save progress in database"""
    update_progress(image, step)

  # Take parameters from database
  image_output = middleware_text_to_image.text_to_image.generate(
    prompt=image.prompt,
    negative_prompt=image.negative_prompt,
    num_steps=image.num_steps,
    callback=callback,
  )
  
  file_name = f"{uuid.uuid4()}.png"
  
  # Upload generated image with random name to bucket.
  storage = minio.Storage()
  storage.upload_image(image_output, file_name, settings.storage_bucket)
  
  update_file_name(image, file_name)
  
  