from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import jwt, JWTError

from core.config import settings

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)

    token = ws.cookies.get("access_token")

    if not token:
        await ws.close(code=1008)
        return

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user = payload.get("sub")
    except JWTError:
        await ws.close()
        return

    try:
        while True:
            data = await ws.receive_text()
            await manager.broadcast(data)

    except WebSocketDisconnect:
        manager.disconnect(ws)
