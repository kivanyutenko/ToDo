from fastapi import FastAPI
from routers import task,folder,user
from db import models
from db.database import engine
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

app.include_router(authentication.router)
app.include_router(task.router)
app.include_router(folder.router)
app.include_router(user.router)

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