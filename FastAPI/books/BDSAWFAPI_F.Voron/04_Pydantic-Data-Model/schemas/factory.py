from datetime import datetime
from pydantic import BaseModel, Field

def list_factory():
  return ["a", "b", "c"]

class Model(BaseModel):
  # Pass a function to the argument without putting arguments on it. 
  # Pydantic will automatically call the function when instantiating a new object.
  # Wrap a function into another function if need to call it with specific arguments
  
  # The first positional argument used for the default value is omitted here. 
  # It's not consistent to have both a default value and a factory. 
  # Pydantic will raise an error if you set those two arguments together.
  
  l: list[str] = Field(default_factory=list_factory)
  d: datetime = Field(default_factory=datetime.now)
  l2: list[str] = Field(default_factory=list)