from fastapi import FastAPI
from routers import task,folder,user, tag
from db import models
from db.database import engine
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app=FastAPI()

app.include_router(authentication.router)
app.include_router(task.router)
app.include_router(folder.router)
app.include_router(user.router)
app.include_router(tag.router)

models.Base.metadata.create_all(engine)

origins = [
  'http://localhost:3000',
  'http://localhost:3001'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)
