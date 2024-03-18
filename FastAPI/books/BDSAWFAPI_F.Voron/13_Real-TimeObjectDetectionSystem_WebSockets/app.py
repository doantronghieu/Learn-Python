from fastapi.responses import FileResponse
import add_packages
import contextlib, asyncio, io, loguru
from fastapi import (
  FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect, staticfiles,
)
from PIL import Image
from models import model

#*=============================================================================
logger = loguru.logger

object_detection = model.ObjectDetection()

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
  object_detection.load_model()
  yield

app = FastAPI(lifespan=lifespan)

#*=============================================================================
@app.post("/object-detection-one-image", response_model=model.Objects)
async def post_object_detection(image: UploadFile = File(...)) -> model.Objects:
  image_object: Image.Image = Image.open(image.file)
  return object_detection.predict(image_object)

#*-----------------------------------------------------------------------------
async def receive(ws: WebSocket, queue: asyncio.Queue):
  # waits for raw bytes from the WebSocket
  while True:
    bytes = await ws.receive_bytes()
    try:
      # adds data to the end of the queue, avoid waiting when the queue is full
      queue.put_nowait(bytes)
    except asyncio.QueueFull:
      # drop data if needed
      pass
    
async def detect(ws: WebSocket, queue: asyncio.Queue):
  # Performs detection on the first message from the queue by running detection 
  # on raw image bytes and sends the result
  while True:
    bytes = await queue.get()
    image: Image.Image = Image.open(io.BytesIO(bytes)) # raw image bytes
    objects: model.Objects = object_detection.predict(image)
    await ws.send_json(objects.model_dump())

@app.websocket("/object-detection")
async def ws_object_detection(ws: WebSocket):
  await ws.accept()
  # Allows to queue data in memory using a FIFO strategy
  # Setting a limit on stored elements helps limit the number of images handled.
  queue: asyncio.Queue = asyncio.Queue(maxsize=1)
  
  task_receive = asyncio.create_task(receive(ws, queue))
  task_detect = asyncio.create_task(detect(ws, queue))
  
  try:
    done, pending = await asyncio.wait(
      {task_receive, task_detect},
      return_when=asyncio.FIRST_COMPLETED,
    )
    
    for task in pending:
      task.cancel()
    for task in done:
      task.result()
  except WebSocketDisconnect:
    pass

#*-----------------------------------------------------------------------------
# allows browsers to query files on the same server
@app.get("/")
async def index():
  return FileResponse("./index.html")


static_files_app = staticfiles.StaticFiles(directory="./assets")
app.mount("/assets", static_files_app)