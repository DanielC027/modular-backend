from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from deps import get_db
from db import schemas

router = APIRouter(prefix="/analisis", tags=["analisis"])


@router.post("/guardar_analisis")
def guardar_analisis(
    q: schemas.AnalisisCreate,
    access_token: str = Cookie(default=None),
):
    print(q.dict())

    if not access_token:
        raise HTTPException(status_code=401, detail="acceso no autorizado")

    return {"msg": "analisis guardado"}
