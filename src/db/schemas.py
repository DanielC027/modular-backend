from pydantic import BaseModel
from typing import List, Dict, Any


class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class ValoresAnalisis(BaseModel):
    probabilidades: List[float]
    etiquetas: List[str]


class AnalisisCreate(BaseModel):
    tipo: str
    fecha: str
    id_escrito: int
    timestamp: int
    huella_digital: str
    valores: ValoresAnalisis
