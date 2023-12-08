from fastapi import FastAPI
from routers import task,folder
from db import models
from db.database import engine

app=FastAPI()

app.include_router(task.router)
#app.include_router(folder.router)

models.Base.metadata.create_all(engine)