from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session

from db import models, schemas
from deps import get_db
from core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    db_user = models.User(
        email=user.email, hashed_password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"msg": "usuario creado"}


@router.post("/login")
def login(user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="credenciales inválidas")

    token = create_access_token({"sub": db_user.email})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        # secure=True en producción
    )

    return {"msg": "login exitoso"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"msg": "logout exitoso"}
