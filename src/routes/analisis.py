from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from deps import get_db
from db import schemas
from db.crud_analisis import guardar_analisis as guardar_analisis_db
from db.crud_analisis import obtener_promedio as obtener_promedio_db
from db.crud_analisis import obtener_promedio_emociones_dia as obtener_emociones_dia_db

router = APIRouter(prefix="/analisis", tags=["analisis"])


@router.post("/guardar_analisis")
def guardar_analisis(
    q: schemas.AnalisisCreate,
    db: Session = Depends(get_db),
    access_token: str = Cookie(default=None),
):
    if not access_token:
        raise HTTPException(status_code=401, detail="acceso no autorizado")

    guardar_analisis_db(db, q)

    return {"msg": "analisis guardado"}


@router.get("/obtener_analisis")
def obtener_analisis(
    fecha: str,
    periodo: str,
    db: Session = Depends(get_db),
    access_token: str = Cookie(default=None),
):
    try:

        if not access_token:
            raise HTTPException(status_code=401, detail="acceso no autorizado")

        huella = "random"

        periodos_validos = {
            "Y": "%Y",
            "M": "%Y-%m",
            "S": "%Y-%W",
        }

        if periodo in periodos_validos:
            return obtener_promedio_db(db, fecha, huella, periodos_validos[periodo])
        elif periodo == "D":
            return obtener_emociones_dia_db(db, fecha, huella)
        else:
            raise HTTPException(status_code=400, detail="parametro no valido")

    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail="error interno del servidor")
