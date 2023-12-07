from fastapi import FastAPI
from routers import task
from db import models
from db.database import engine

app=FastAPI()

app.include_router(task.router)

models.Base.metadata.create_all(engine)