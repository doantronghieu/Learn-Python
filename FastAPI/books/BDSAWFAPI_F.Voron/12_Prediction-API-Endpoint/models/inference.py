import os
import joblib
from typing import Union
from pydantic import BaseModel
from sklearn.pipeline import Pipeline

#*-----------------------------------------------------------------------------
class PredictionInput(BaseModel):
  text: str
  
class PredictionOutput(BaseModel):
  category: str

#*-----------------------------------------------------------------------------
# Joblib saves cached results on the hard disk automatically
memory = joblib.Memory(location="cache.joblib")

@memory.cache(ignore=["model"])  # enables Joblib caching
# Excluded the model argument since Joblib cannot dump complex objects
def predict(model: Pipeline, text: str) -> int:
  """
  Whenever function called, Joblib checks if result on disk for same arguments. 
  Returns directly if found, otherwise proceeds with regular function call.
  """
  prediction = model.predict([text])[0]
  # category index
  return prediction

#*-----------------------------------------------------------------------------
class MyModel:
  model: Union[Pipeline, None] = None
  targets: Union[list[str], None] = None
  
  def load_model(self) -> None:
    """Loads the model""" 

    # Load the model
    model_file = os.path.join(os.path.dirname(__file__), "model.joblib")
    # scikit-learn estimator with training parameters and a list of categories
    loaded_model : tuple[Pipeline, list[str]] = joblib.load(model_file)
    model, targets = loaded_model
    self.model = model
    self.targets = targets

  async def predict(self, input: PredictionInput) -> PredictionOutput:
    """
    Runs a prediction. Injected into the path operation function. 
    Directly accepting PredictionInput from FastAPI.
    """

    if not self.model or not self.targets:
      raise RuntimeError("Model is not loaded.")
  
    prediction = predict(self.model, input.text)
    category = self.targets[prediction]
    
    return PredictionOutput(category=category)

  def clear_cache(self):
    # removes all Joblib cache files on the disk
    memory.clear()
#*-----------------------------------------------------------------------------

