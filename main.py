from fastapi import FastAPI
from routers import task,folder,user
from db import models
from db.database import engine
from auth import authentication


app=FastAPI()

app.include_router(authentication.router)
app.include_router(task.router)
app.include_router(folder.router)
app.include_router(user.router)

models.Base.metadata.create_all(engine)