# generated by datamodel-codegen:
#   filename:  brep_entity_schema.json
#   timestamp: 2024-06-20T03:50:19+00:00

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Aabb(BaseModel):
    min: List[float]
    max: List[float]


class Vertice(BaseModel):
    handler: int
    x: float
    y: float
    z: float


class Face(BaseModel):
    handler: int
    plane: List[float] = Field(..., description='normal3d and D')
    surface: Optional[int] = None
    edges: List[int]


class Surface(BaseModel):
    handler: int
    type: int = Field(..., description='0~4')
    data: Optional[Dict[str, Any]] = None


class Edge(BaseModel):
    handler: int
    vertex: int = Field(..., description='vertex handler')
    partner: Optional[int] = Field(None, description='coedge handler')
    face: int = Field(..., description='parent face handler')
    curve: Optional[int] = Field(None, description='curve handler')


class Curve(BaseModel):
    handler: int
    type: int = Field(..., description='0,1')
    data: Optional[Dict[str, Any]] = None


class Body(BaseModel):
    handler: int = Field(..., description='uniq id')
    aabb: Aabb = Field(..., title='AABB')
    vertices: List[Vertice]
    faces: List[Face]
    surfaces: List[Surface]
    edges: List[Edge]
    curves: List[Curve]


class BrepContext(BaseModel):
    bodies: List[Body]


class Savea(BaseModel):
    url: str
    transformer: Optional[str] = None


class ModelerBrep(BaseModel):
    brepContext: BrepContext = Field(..., title='BrepContext')
    saveas: List[Savea]
