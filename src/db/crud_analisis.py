from sqlalchemy.orm import Session
from sqlalchemy import func
from db import models


def guardar_analisis(db: Session, data):

    # 0. Guardar escrito
    escrito = (
        db.query(models.Escrito)
        .filter_by(fecha=data.fecha, huella_digital=data.huella_digital)
        .first()
    )

    if not escrito:
        escrito = models.Escrito(fecha=data.fecha, huella_digital=data.huella_digital)
        db.add(escrito)
        db.commit()
        db.refresh(escrito)

    # 1. Obtener o crear analisis
    analisis = db.query(models.Analisis).filter_by(id_escrito=data.id_escrito).first()

    if not analisis:
        analisis = models.Analisis(id_escrito=data.id_escrito)
        db.add(analisis)
        db.commit()
        db.refresh(analisis)

    # 2. Procesar emociones
    etiquetas = data.valores.etiquetas
    probabilidades = data.valores.probabilidades

    for i, emocion_nombre in enumerate(etiquetas):

        emocion = db.query(models.Emocion).filter_by(nombre=emocion_nombre).first()

        if not emocion:
            emocion = models.Emocion(nombre=emocion_nombre)
            db.add(emocion)
            db.commit()
            db.refresh(emocion)

        porcentaje = probabilidades[i]
        # print(analisis)
        relacion = (
            db.query(models.ListaEmociones)
            .filter_by(id_analisis=analisis.id_analisis, id_emocion=emocion.id_emocion)
            .first()
        )

        if relacion:
            relacion.porcentaje_emocion = porcentaje
        else:
            nueva = models.ListaEmociones(
                id_analisis=analisis.id_analisis,
                id_emocion=emocion.id_emocion,
                porcentaje_emocion=porcentaje,
            )
            db.add(nueva)

    db.commit()

    return analisis


def obtener_promedio(db, fecha, huella, formato):
    try:
        return (
            db.query(
                models.ListaEmociones.id_emocion,
                models.Emocion.nombre,
                func.avg(models.ListaEmociones.porcentaje_emocion).label("promedio"),
                func.count().label("total"),
            )
            .join(models.Analisis)
            .join(models.Escrito)
            .join(models.Emocion)
            .filter(
                func.strftime(formato, models.Escrito.fecha)
                == func.strftime(formato, fecha),
            )
            .group_by(models.ListaEmociones.id_emocion, models.Emocion.nombre)
            .all()
        )
        """ .filter(
                models.Escrito.huella_digital == huella,
                func.strftime(formato, models.Escrito.fecha)
                == func.strftime(formato, fecha),
            ) """
    except Exception as ex:
        print("Error al obtener datos promedio analisis bd: ", ex)


def obtener_promedio_emociones_dia(db: Session, fecha, huella):
    try:
        resultados = (
            db.query(models.Emocion.nombre, models.ListaEmociones.porcentaje_emocion)
            .join(models.Analisis)
            .join(models.Escrito)
            .join(models.Emocion)
            .filter(models.Escrito.fecha == fecha)
            .all()
        )
        # .filter(models.Escrito.fecha == fecha, models.Escrito.huella_digital == huella)
        return resultados
    except Exception as ex:
        print("Error al obtener datos promedio dia analisis bd: ", ex)
