from fastapi import FastAPI
from routers.main_router import router as main_router

app = FastAPI()
app.include_router(main_router, prefix="/main", tags=["main"])
