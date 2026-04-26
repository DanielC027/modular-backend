from fastapi import APIRouter, Depends, HTTPException, Cookie, Query, Request
from typing import Annotated
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
    request: Request,
    fecha: Annotated[
        str,
        Query(
            max_length=10,
            pattern=r"^\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\d|30)|02-(?:0[1-9]|1\d|2[0-8]))$",
        ),
    ],
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        access_token = request.cookies.get("access_token")
        # print("datos solicitados, access_token: ", access_token)
        if not access_token:
            raise HTTPException(status_code=401, detail="acceso no autorizado")

        huella = "random"

        periodos_validos = {
            "Y": "%Y",
            "M": "%Y-%m",
            "W": "%Y-%W",
        }

        if periodo in periodos_validos:
            # print("Periodo: ", periodo)
            result = obtener_promedio_db(db, fecha, huella, periodos_validos[periodo])
            # print(result)
            etiquetas = [etiqueta[1] for etiqueta in result]
            probabilidades = [etiqueta[2] for etiqueta in result]
            msj = {
                "fecha": fecha,
                "tipo": "analisis_emociones",
                "valores": {"etiquetas": etiquetas, "probabilidades": probabilidades},
            }
            return msj
            # return [row._asdict() for row in result]
        elif periodo == "D":
            # print("Periodo: dia")
            result = obtener_emociones_dia_db(db, fecha, huella)
            # print(result)
            etiquetas = [etiqueta[0] for etiqueta in result]
            probabilidades = [etiqueta[1] for etiqueta in result]
            msj = {
                "fecha": fecha,
                "tipo": "analisis_emociones",
                "valores": {"etiquetas": etiquetas, "probabilidades": probabilidades},
            }
            return msj
            # return [row._asdict() for row in result]
        else:
            raise HTTPException(status_code=400, detail="parametro no valido")

    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail="error interno del servidor")
