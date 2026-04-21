from fastapi import APIRouter, WebSocket
from jose import jwt, JWTError

from core.config import settings

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    token = ws.cookies.get("access_token")

    if not token:
        await ws.close()
        return

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user = payload.get("sub")

    except JWTError:
        await ws.close()
        return

    while True:
        data = await ws.receive_text()
        await ws.send_text(f"{user}: {data}")
