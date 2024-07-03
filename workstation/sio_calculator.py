import socketio
import sys
from pathlib import Path
from loguru import logger
from manager import Manager

sys.path.append(str((Path(__file__) / "../../").resolve()))
sys.path.append(str((Path(__file__) / "../../../modeler-pybind").resolve()))

import modeler


def init(sio, manager: Manager):
    @sio.event
    async def calculatorCreate(socketid, initValue: float = 0):
        logger.debug(f"calculatorCreate: {socketid}, {initValue} ")
        calc = modeler.Calculator(initValue)
        manager.contexts.set(socketid, calc)
        await sio.emit('onCalculatorCreate', {"socketid": socketid, 'status': "OK"})

    @sio.event
    async def calculatorRun(socketid, data):
        logger.debug(f"calculatorRun: {socketid}, {data}")
        manager.contexts.heartbeat(socketid)
        calc: modeler.Calculator = manager.contexts.get(socketid)
        op = getattr(calc, data.get("op"))
        if callable(op):
            op(data.get("value"))
        await sio.emit('onCalculatorRun', {"socketid": socketid, "result": calc.getCurrent(), 'status': "OK"})
