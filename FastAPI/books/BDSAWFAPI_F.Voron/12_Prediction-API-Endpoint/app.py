import add_packages
import contextlib
from fastapi import FastAPI, Depends, status
from models import inference
from routers import prediction_router

#*-----------------------------------------------------------------------------
my_model = inference.MyModel()

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
  # Load the model when the app is run
  my_model.load_model()
  yield

app = FastAPI(lifespan=lifespan)

@app.post("/prediction")
async def predict(
  input: inference.PredictionInput,
) -> inference.PredictionOutput:
  output = await my_model.predict(input)
  return output

@app.delete("/cache", status_code=status.HTTP_204_NO_CONTENT)
def delete_cache():
  my_model.clear_cache()
# *-----------------------------------------------------------------------------
