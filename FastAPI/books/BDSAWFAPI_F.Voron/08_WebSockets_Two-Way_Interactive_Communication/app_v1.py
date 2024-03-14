import asyncio, contextlib
from broadcaster import Broadcast
from datetime import datetime
from pydantic import BaseModel
from starlette.websockets import WebSocketDisconnect
from fastapi import HTTPException, WebSocket, Cookie, WebSocketException, status
from fastapi import FastAPI


#*-----------------------------------------------------------------------------
API_TOKEN = "SECRET"

broadcast = Broadcast("redis://localhost:6380")
# Channel for publishing and subscribing to messages
# Use dynamic channel names for real-world applications
CHANNEL = "CHAT"

# Open/Close connection with broker when starting/exiting application
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
  await broadcast.connect()
  yield
  await broadcast.disconnect()

app = FastAPI(lifespan=lifespan)

#*-----------------------------------------------------------------------------
# Structure the data (message, username) in a message instead of raw string
class MessageEvent(BaseModel):
  username: str
  message: str

#*-----------------------------------------------------------------------------
async def receive_message(websocket: WebSocket, username: str):
  # Subscribes to the broadcast channel and waits for `event` messages
  async with broadcast.subscribe(channel=CHANNEL) as subscriber:
    async for event in subscriber:
      # Deserialize serialized JSON Data message
      message_event = MessageEvent.model_validate_json(event.message)
      # Discard user's own messages
      # Rely on a unique user ID instead of a username in production
      if message_event.username != username:
        # Parses the JSON, instantiate a MessageEvent object
        # Automatic serialization of object
        await websocket.send_json(message_event.model_dump())

async def send_message(websocket: WebSocket, username: str):
  # Waits for new data sent by client in the socket in plain text format
  data = await websocket.receive_text()
  event = MessageEvent(username=username, message=data) # structuring data
  # Send back the message to the client
  await broadcast.publish(channel=CHANNEL, message=event.model_dump_json())

#*-----------------------------------------------------------------------------
@app.websocket("/ws")
# Websocket decorator to create a WebSocket endpoint
async def websocket_endpoint(
  # Object has methods to work with the WebSocket
  websocket: WebSocket,
  username: str = "Anonymous",
):
  
  # Accept first to inform the client of agreement to open the tunnel
  await websocket.accept()
  
  # Handle client disconnection
  try:
    # Communication channel remains open for exchanging multiple messages until
    # either the client or server decides to close it
    while True:
      # Block server and wait until data is received from client
      # The process can respond to other client requests by event loop.
      
      # Define coroutines. Transform coroutine into task object
      # Task (event loop) manages execution of coroutine
      task_receive_message = asyncio.create_task(
        receive_message(websocket, username)
      )
      task_send_message = asyncio.create_task(
        send_message(websocket, username)
      )
      
      # Running tasks concurrently. Blocks until all tasks are done by default
      done, pending = await asyncio.wait(
        {task_receive_message, task_send_message},
        # Block until one of the tasks is completed
        return_when=asyncio.FIRST_COMPLETED,
      )
      for task in pending: # tasks not yet completed
        # Cancel all pending tasks to prevent them from piling up at each iteration
        task.cancel()
      for task in done: # completed tasks
        # returns the result of the coroutine, re-raises an exception (if have) inside
        task.result()
      
      # Go back to the start of the loop to start again wait for another message 
  except WebSocketDisconnect:
    pass

#*-----------------------------------------------------------------------------
