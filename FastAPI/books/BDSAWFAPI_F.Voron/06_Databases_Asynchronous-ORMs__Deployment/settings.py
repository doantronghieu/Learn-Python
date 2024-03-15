from pydantic import ConfigDict

class Settings(ConfigDict):
  debug: bool = False
  environment: str
  database_url : str
  
  class Config:
    env_file = ".env"
    
settings = Settings()