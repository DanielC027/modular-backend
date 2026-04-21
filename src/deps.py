from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from db.database import SessionLocal
from db import models
from core.config import settings


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        email = payload.get("sub")

        user = db.query(models.User).filter(models.User.email == email).first()

        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
