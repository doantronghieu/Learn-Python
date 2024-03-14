import asyncio, contextlib
from broadcaster import Broadcast
from datetime import datetime
from pydantic import BaseModel
from starlette.websockets import WebSocketDisconnect
from fastapi import HTTPException, WebSocket, Cookie, WebSocketException, status
from fastapi import FastAPI


#*-----------------------------------------------------------------------------
API_TOKEN = "SECRET"

#*-----------------------------------------------------------------------------
app = FastAPI()

#*-----------------------------------------------------------------------------

async def echo_message(websocket: WebSocket):
  # Returns data sent by client in plain text format
  data = await websocket.receive_text()
  # Send back the message to the client
  await websocket.send_text(f"Message: {data}")

async def send_time(websocket: WebSocket):
  await asyncio.sleep(10)
  await websocket.send_text(f"Time: {datetime.now()}")

@app.websocket("/ws")
# Websocket decorator to create a WebSocket endpoint
async def websocket_endpoint(
  # Object has methods to work with the WebSocket
  websocket: WebSocket,
  username: str = "Anonymous",
  token: str = Cookie(...),
):
  # Dummy authentication logic
  if token != API_TOKEN:
    raise HTTPException(status.WS_1008_POLICY_VIOLATION)
  
  # Accept first to inform the client of agreement to open the tunnel
  await websocket.accept()
  
  await websocket.send_text(f"Hello {username}")
  
  # Handle client disconnection
  try:
    # Communication channel remains open for exchanging multiple messages until
    # either the client or server decides to close it
    while True:
      # Block server and wait until data is received from client
      # The process can respond to other client requests by event loop.
      
      # Define coroutines. Transform coroutine into task object
      # Task (event loop) manages execution of coroutine
      
      # One will wait for a client message, the other will wait for 10 seconds. 
      # If the client sends a message before 10 seconds, it will be sent back. 
      # Otherwise, the send_time coroutine will send the current time
      task_echo_message = asyncio.create_task(echo_message(websocket))
      task_send_time = asyncio.create_task(send_time(websocket))
      
      # Running tasks concurrently. Blocks until all tasks are done by default
      done, pending = await asyncio.wait(
        {task_echo_message, task_send_time},
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
