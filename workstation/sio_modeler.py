from loguru import logger

from manager import Manager
from modeler_context import ModelerContext


def init(sio, manager: Manager):
    @sio.event
    async def documentLoadBrep(sid, args):
        documentid = args[0] if isinstance(args, list) else args
        logger.debug(f"documentLoadBrep , {sid}, {documentid}")
        context = manager.contexts.get(documentid)
        await sio.emit('on_documentLoadBrep', {'status': "OK", "documentid": documentid, "context": context.toBrepJson()})

    @manager.help("update document geometry scene data in 3d", ["This cmd will send all geometry data in mesh to client."])
    @sio.event
    async def documentLoadScene(sid, args):
        documentid = args[0] if isinstance(args, list) else args
        logger.debug(f"documentLoadScene , {sid}, {documentid}")
        context = manager.contexts.get(documentid)
        if context is None:
            context = ModelerContext(documentid)
            manager.contexts.set(documentid, context)
        context.sockets.append(sid)
        await sio.emit('on_documentLoadScene', {'status': "OK", "documentid": documentid, "context": context.toSceneJson()})

    @manager.help("create body", [
        "samples:",
        '    ["sphere", 0,0,0, 1.0, 32] : create a sphere on (0,0,0) with radius=1, segments=32',
        '    ["box", 0,0,0,  1,1,1] : create a box on position=(0,0,0) with vector=(1,1,1)'])
    @sio.event
    async def bodyCreate(sid, args):
        logger.debug(f"bodyCreate , {sid},args={args}")
        try:
            documentid, type, *type_param = args
            context: ModelerContext = manager.contexts.get(documentid)
            bodyUpdates = context.bodyCreate(type, type_param)
            await sio.emit('on_bodyCreate', {"handler": list(map(lambda body: body.handler(), bodyUpdates))})
        except Exception as err:
            logger.warning(str(err))
            await sio.emit("on_error", str(err))

    @manager.help("body boolean", ["two body boolean operation, include add/sub/intersect",
                                   "example:['add', 2, 40]"])
    @sio.event
    async def bodyBoolean(sid, args):
        logger.debug(f"bodyBoolean , {sid}, args={args}")
        try:
            documentid, type, bodyA_id, bodyB_id = args
            context: ModelerContext = manager.contexts.get(documentid)
            if not context:
                return await sio.emit("on_error", 'no context')
            bodyHandlers = list(map(lambda body: body.handler(), context.bodies))
            bodyA = context.bodies[bodyHandlers.index(bodyA_id)]
            bodyB = context.bodies[bodyHandlers.index(bodyB_id)]
            bodyUpdates = context.bodyBoolean(type, bodyA, bodyB)
            await sio.emit('on_bodyBoolean', {"handler": list(map(lambda body: body.handler(), bodyUpdates))})
        except Exception as err:
            logger.warning(str(err))
            await sio.emit("on_error", str(err))


    @manager.help("get body info", ["empty parameter will give out all body handlers",
                                    "the body full brep info will be given if specified body handler. only returns the first one if multiple handlers.",
                                    "example: [2]"])
    @sio.event
    async def bodyInfo(sid, args):
        logger.debug(f"bodyInfo, {sid},args={args}")
        documentid, *bodyIds = args
        print(manager.contexts)
        context: ModelerContext = manager.contexts.get(documentid)
        if not context:
            return await sio.emit("on_bodyInfo", [])
        bodyHandlers = list(map(lambda body: body.handler(), context.bodies))
        if len(bodyIds) == 0:
            return await sio.emit('on_bodyInfo', bodyHandlers)

        bodyId = bodyIds[0]
        if bodyId in bodyHandlers:
            body = context.bodies[bodyHandlers.index(bodyId)]
            await sio.emit('on_bodyInfo', context.bodyInfo(body))
        else:
            await sio.emit('on_error', f"can not find this body: {bodyId}")

    @manager.help("set transform to body", ["transform body",
                                            'example: ["translate", 2, 10,0,0] will move x=10 for body id=2',
                                            '["rotate", bodyId, line_p0_x, line_p0_y, line_p0_z, line_dir_x, line_dir_y, line_dir_z,angle]',
                                            '["element",bodyId, 16 times transformElementNumber], where transformElement is 1x16 numbers'])
    @sio.event
    async def bodyTransform(sid, args):
        logger.debug(f"bodyTransform, {sid},args={args}")
        try:
            documentid, transform_type, body_id, *transformInfo = args
            context: ModelerContext = manager.contexts.get(documentid)
            if not context:
                return await sio.emit("on_error", 'no context')
            bodyHandlers = list(map(lambda body: body.handler(), context.bodies))
            body = context.bodies[bodyHandlers.index(body_id)]
            bodyUpdates = context.bodyTransform(transform_type,body,transformInfo)
            await sio.emit('on_bodyTransform', {"handler": list(map(lambda body: body.handler(), bodyUpdates))})
        except Exception as err:
            logger.warning(str(err))
            await sio.emit("on_error", str(err))