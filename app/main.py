from fastapi import FastAPI
from . import models
from .database import engine
from .routers import tasks, users, auth
from .config import settings

models.Base.metadata.create_all(bind = engine)

app = FastAPI(title = "Заметки")


app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello"}