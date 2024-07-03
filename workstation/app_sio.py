import datetime, sys, os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import socketio
import sio_calculator
import sio_common
import sio_modeler

from cache import gCache
from manager import Manager

logger.add(sys.stdout, format="{time} {level} {message}", level="DEBUG")
logger.add(os.path.join("../log", "app_sio/{time:YYYY}_{time:MM}_{time:DD}.log"), rotation="0:00")

app = FastAPI(separate_input_output_schemas=False)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 服务启动时间
serverStartTime = str(datetime.datetime.now())

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*', cors_credentials=True)
socket_app = socketio.ASGIApp(sio)
app.mount("/", socket_app)

manager = Manager()

sio_calculator.init(sio, manager)
sio_modeler.init(sio, manager)
sio_common.init(sio, manager)  # common 由于需要构造help, 必须放到最后

logger.info(f"------------- WS SERVER STARTS at {serverStartTime},  ----------")
