from fastapi import APIRouter, Depends
from db import models
from deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_me(current_user: models.User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}
