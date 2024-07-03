"""

        Pybind11 Modeler plugin
        -----------------------

        .. currentmodule:: modeler

    
"""
from __future__ import annotations
import numpy
import typing
__all__ = ['Body', 'Calculator', 'Edge', 'Entity', 'Face', 'Interval3d', 'Line3d', 'ModelerAPI', 'Plane', 'Point3d', 'Surface', 'SurfaceType', 'Transform3d', 'Vector3d', 'Vertex', 'add', 'subtract']
class Body(Entity):
    @staticmethod
    @typing.overload
    def box(arg0: Point3d, arg1: Vector3d) -> Body:
        """
        create box, args: corner, size
        """
    @staticmethod
    @typing.overload
    def box(arg0: float, arg1: float, arg2: float, arg3: float, arg4: float, arg5: float) -> Body:
        ...
    @staticmethod
    @typing.overload
    def cylinder(arg0: Line3d, arg1: float, arg2: int) -> Body:
        """
        create cylinder, args: axis, radius, approximate
        """
    @staticmethod
    @typing.overload
    def cylinder(arg0: float, arg1: float, arg2: float, arg3: float, arg4: float, arg5: float, arg6: float, arg7: int) -> Body:
        ...
    @staticmethod
    @typing.overload
    def sphere(arg0: Point3d, arg1: float, arg2: int) -> Body:
        """
        create sphere, args: center, radius, approximate
        """
    @staticmethod
    @typing.overload
    def sphere(arg0: float, arg1: float, arg2: float, arg3: float, arg4: int) -> Body:
        ...
    def __iadd__(self, arg0: Body) -> Body:
        """
        boolean operator +=, union
        """
    def __imul__(self, arg0: Body) -> Body:
        """
        boolean operator *=, intersect
        """
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: Body) -> None:
        ...
    def __isub__(self, arg0: Body) -> Body:
        """
        boolean operator -=, subtract
        """
    def aabb(self, arg0: float) -> Interval3d:
        ...
    def combine(self, arg0: Body) -> Body:
        """
        combine
        """
    def copy(self) -> Body:
        ...
    def faceCount(self) -> int:
        """
        get face count
        """
    def isValid(self, arg0: int) -> bool:
        """
        arg should be 1
        """
    def transform(self, arg0: Transform3d) -> Body:
        ...
class Calculator:
    """
    class for calc
    """
    def __init__(self, arg0: float) -> None:
        ...
    def divideBy(self, arg0: float) -> Calculator:
        ...
    def getCurrent(self) -> float:
        """
        get result
        """
    def minus(self, arg0: float) -> Calculator:
        ...
    def plus(self, arg0: float) -> Calculator:
        """
        add two float numbers
        """
    def reset(self, arg0: float) -> Calculator:
        """
        reset to 0
        """
    def times(self, arg0: float) -> Calculator:
        """
        times
        """
class Edge(Entity):
    def __init__(self) -> None:
        ...
    def vertex(self) -> Vertex:
        """
        get Edge vertex
        """
class Entity:
    def handler(self) -> int:
        """
        get uniq handler
        """
class Face(Entity):
    def __init__(self) -> None:
        ...
    def edgeCount(self) -> int:
        ...
    def plane(self) -> Plane:
        ...
    def surface(self) -> Surface:
        """
        get surface , maybe NULL
        """
class Interval3d:
    max: Point3d
    min: Point3d
class Line3d:
    point: Point3d
    vector: Vector3d
    @typing.overload
    def __init__(self, arg0: Point3d, arg1: Point3d) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: Point3d, arg1: Vector3d) -> None:
        ...
class ModelerAPI:
    @staticmethod
    def ExtractBodyBrep(arg0: Body) -> str:
        ...
    @staticmethod
    def ExtractBodyMesh(arg0: Body) -> str:
        ...
    @staticmethod
    def getBodyFaces(arg0: Body) -> list[Face]:
        ...
    @staticmethod
    def getBodySurfaces(arg0: Body) -> list[Surface]:
        ...
    @staticmethod
    def getBodyVertices(arg0: Body) -> list[Vertex]:
        ...
    @staticmethod
    def getFaceEdgeLoops(arg0: Face) -> list[Edge]:
        ...
class Plane:
    d: float
    normal: Vector3d
    def __init__(self) -> None:
        ...
class Point3d:
    x: float
    y: float
    z: float
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: float, arg1: float, arg2: float) -> None:
        ...
class Surface(Entity):
    def type(self) -> SurfaceType:
        """
        get surface type, 0~4
        """
class SurfaceType:
    """
    Members:
    
      Unspecified
    
      Cylinder
    
      Cone
    
      Sphere
    
      Torus
    """
    Cone: typing.ClassVar[SurfaceType]  # value = <SurfaceType.Cone: 2>
    Cylinder: typing.ClassVar[SurfaceType]  # value = <SurfaceType.Cylinder: 1>
    Sphere: typing.ClassVar[SurfaceType]  # value = <SurfaceType.Sphere: 3>
    Torus: typing.ClassVar[SurfaceType]  # value = <SurfaceType.Torus: 4>
    Unspecified: typing.ClassVar[SurfaceType]  # value = <SurfaceType.Unspecified: 0>
    __members__: typing.ClassVar[dict[str, SurfaceType]]  # value = {'Unspecified': <SurfaceType.Unspecified: 0>, 'Cylinder': <SurfaceType.Cylinder: 1>, 'Cone': <SurfaceType.Cone: 2>, 'Sphere': <SurfaceType.Sphere: 3>, 'Torus': <SurfaceType.Torus: 4>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Transform3d:
    @staticmethod
    def rotation(arg0: Line3d, arg1: float) -> Transform3d:
        ...
    @staticmethod
    def translation(arg0: Vector3d) -> Transform3d:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        create identify 4x4 transform
        """
    @typing.overload
    def __init__(self, arg0: Point3d) -> None:
        """
        create a transrom with origin point
        """
    @typing.overload
    def __init__(self, arg0: Point3d, arg1: Vector3d, arg2: Vector3d, arg3: Vector3d) -> None:
        """
        create transform with origin, xDir, ydir,zdir
        """
    def getCoordSystem(self, arg0: Point3d, arg1: Vector3d, arg2: Vector3d, arg3: Vector3d) -> None:
        ...
    @property
    def elements(self) -> numpy.ndarray:
        ...
    @elements.setter
    def elements(self) -> None:
        ...
class Vector3d:
    x: float
    y: float
    z: float
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: float, arg1: float, arg2: float) -> None:
        ...
class Vertex(Entity):
    def __init__(self) -> None:
        ...
    def point(self) -> Point3d:
        """
        get Point3d
        """
def add(arg0: int, arg1: int) -> int:
    """
            Add two numbers
    
            Some other explanation about the add function.
    """
def subtract(arg0: int, arg1: int) -> int:
    """
            Subtract two numbers
    
            Some other explanation about the subtract function.
    """
