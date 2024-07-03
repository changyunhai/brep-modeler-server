from loguru import logger

from manager import Manager

count = 1


# ---------------SOCKETIO common:---------------
def init(sio, manager: Manager):
    @sio.event
    async def connect(socketid, environ):
        logger.debug(f"connect {socketid}")
        await sio.emit('on_connect', {'status': "OK", "socketid": socketid})

    @sio.event
    def disconnect(socketid):
        logger.debug(f'disconnect {socketid}')

    @sio.event
    async def documents(socketid, data):
        global count
        count += 1
        logger.debug(f'manager {socketid}, {data}, returns count={count}')

        await sio.emit('on_documents', {"documents": list(manager.contexts.keys()), "count": count})


    @manager.help("list all commands: ", lambda m: list(manager.helps.keys()))
    @sio.event
    async def help(sid, args):
        logger.debug(f"help , {sid},args={args}")
        documentid, *types = args
        type = types[0] if types is not None and len(types) > 0 else "help"
        msg = manager.helps.get(type)

        await sio.emit("on_help", msg)
