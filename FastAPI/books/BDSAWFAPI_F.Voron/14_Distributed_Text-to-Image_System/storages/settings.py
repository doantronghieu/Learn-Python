import add_packages
import os
from pydantic import ConfigDict, BaseModel
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

class Settings(BaseModel):
  model_config = ConfigDict(extra="ignore")
  
  database_url: str
  storage_endpoint: str
  storage_access_key: str
  storage_secret_key: str
  storage_bucket: str

settings = Settings(
  database_url=os.getenv("DATABASE_URL"),
  storage_access_key=os.getenv("STORAGE_ACCESS_KEY"),
  storage_bucket=os.getenv("STORAGE_BUCKET"),
  storage_endpoint=os.getenv("STORAGE_ENDPOINT"),
  storage_secret_key=os.getenv("STORAGE_SECRET_KEY"),
)