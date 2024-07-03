import sys, json
from pathlib import Path

sys.path.append(str((Path(__file__) / "../../").resolve()))
sys.path.append(str((Path(__file__) / "../../../modeler-pybind").resolve()))

from modeler import Body, Point3d, Vector3d, ModelerAPI, Line3d, Transform3d


class ModelerContext:
    def __init__(self, documentid: str):
        self.documentid: str = documentid
        self.sockets: list[str] = []
        self.bodies: list[Body] = []
        pass

    def bodyCreate(self, type: str, typeparam: list[any]) -> list[Body]:
        body = None
        # typeparam = list(map(lambda p: float(p), typeparam))
        if hasattr(Body, type):
            method = getattr(Body, type)
            body = method(*typeparam)
        else:
            raise Exception(f" can not find {type} in Body !")

        if body is not None:
            self.bodies.append(body)
        return [body]

    def bodyInfo(self, body: Body):
        bodyJsonStr = ModelerAPI.ExtractBodyBrep(body)
        bodyJson = json.loads(bodyJsonStr)
        return bodyJson

    def bodyBoolean(self, operator: str, bodyA: Body, bodyB: Body) -> list[Body]:
        if operator == "add":
            bodyA += bodyB
        elif operator == "sub":
            bodyA -= bodyB
        elif operator == 'intersect':
            bodyA *= bodyB
        return [bodyA, bodyB]

    def bodyTransform(self, operator: str, body: Body, param: list[float]) -> list[Body]:
        if operator == 'translate':
            translate = Transform3d.translation(Vector3d(param[0], param[1], param[2]))
            print("translate=", translate.elements)
            body.transform(translate)
        return [body]

    def toSceneJson(self) -> dict:
        print("bodies=", list(map(lambda body: body.handler(), self.bodies)))
        children = []
        for body in self.bodies:
            bodyJsonStr = ModelerAPI.ExtractBodyMesh(body)
            bodyJson = json.loads(bodyJsonStr)
            children.append(bodyJson)
        contextJson = {"scene": {"children": children}, "sockets": self.sockets}
        return contextJson

    def toBrepJson(self) -> dict:
        print("bodies=", list(map(lambda body: body.handler(), self.bodies)))
        children = []
        for body in self.bodies:
            bodyJsonStr = ModelerAPI.ExtractBodyBrep(body)
            bodyJson = json.loads(bodyJsonStr)
            children.append(bodyJson)
        contextJson = {"brep": {"bodies": children}, "sockets": self.sockets}
        return contextJson
