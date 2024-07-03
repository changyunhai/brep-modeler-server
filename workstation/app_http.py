import asyncio
import datetime, sys, os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from fastapi import APIRouter
import socketio

logger.add(sys.stdout, format="{time} {level} {message}", level="DEBUG")
logger.add(os.path.join("../log", "app_http/{time:YYYY}_{time:MM}_{time:DD}.log"), rotation="0:00")
serverStartTime = str(datetime.datetime.now())  # 服务启动时间

app = FastAPI(separate_input_output_schemas=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义业务路由
default_router = APIRouter(prefix="/pybind")
app.include_router(router=default_router)

sio = socketio.Client()
manager = None


# ---------------FASTAPIS---------------

@default_router.get('/', tags=["common"])
@app.get('/', tags=["common"])
def home():
    return f"pybind server，启动时间：{serverStartTime}"


@default_router.get("/cache", tags=["common"])
@app.get('/cache', tags=["common"])
async def ws_connections():
    sio.emit("manager", {"type": "get"})
    await asyncio.sleep(0.5)
    logger.info(f"ws_connections: {manager}")
    return manager


@sio.event
def onManager(data):
    global manager
    manager = data
    print(f"onManager,  {data}")


sio.connect('http://localhost:8810/')
logger.info(f"------------- HTTP SERVER STARTS at {serverStartTime},  ----------")
