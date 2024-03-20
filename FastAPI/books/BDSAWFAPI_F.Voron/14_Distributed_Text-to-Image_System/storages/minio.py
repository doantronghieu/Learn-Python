import add_packages
from loguru import logger
import io
import datetime
import minio
from PIL import Image
from settings import settings

class Storage:
  """
  Wrapper around the MinIO client. 
  Use it to upload images and get a pre-signed URL from the API
  """
  def __init__(self) -> None:
    self.client = minio.Minio(
      endpoint=settings.storage_endpoint,
      access_key=settings.storage_access_key,
      secret_key=settings.storage_secret_key,
    )
  
  def ensure_bucket(self, bucket_name: str):
    """
    Ensures the correct bucket is created in object storage. 
    
    In S3, a bucket is like a folder where can store files, and each uploaded 
    file must go into a bucket.
    """
    is_bucket_exists = self.client.bucket_exists(bucket_name)
    if not is_bucket_exists:
      self.client.make_bucket(bucket_name)
      logger.info(f"Creating bucket `{bucket_name}`")
    logger.info(f"Found bucket `{bucket_name}`")
  
  def upload_image(
    self, 
    image: Image.Image, # Pillow Image (model's result)
    object_name: str, 
    bucket_name: str,
  ):
    """Uploads an image to the storage"""
    self.ensure_bucket(bucket_name)
    
    # Converts Image into a raw stream of bytes for S3 upload
    image_data = io.BytesIO()
    image_data_length = len(image_data.getvalue())
    image.save(image_data, format="PNG")
    image_data.seek(0)
    
    self.client.put_object(
      bucket_name=bucket_name,
      object_name=object_name,
      data=image_data,
      length=image_data_length,
      content_type="image/png",
    )
  
  def get_presigned_url(
    self,
    object_name: str,
    bucket_name: str,
    *,
    expires: datetime.timedelta = datetime.timedelta(days=7)
  ) -> str:
    """
    Generate a pre-signed URL for a specific file in a specific bucket for a set
    period of time on API server using the S3 client with a temporary access key
    to authenticate the user and verify their rights before granting access.    
    """
    return self.client.presigned_get_object(
      bucket_name=bucket_name, object_name=object_name, expires=expires,
    )