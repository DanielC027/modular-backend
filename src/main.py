from fastapi import FastAPI
from db.database import Base, engine

from routes import auth, users, ws

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ws.router)
