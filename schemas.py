from datetime import date, datetime, time
from pydantic import BaseModel

class TaskBase(BaseModel):
    title:str='Task'
    description:str='Something to do'

class TaskDisplay(BaseModel):
    title:str
    description:str
    task_status:str
    priority:str
    flag:bool
    date:date
    time:time
    folder_id:int 

    class Config:
      orm_mode = True
      json_encoders = {
            date: lambda v: v.strftime("%d.%m.%Y"),
            time: lambda v: v.strftime("%H:%M")
        }


class FolderDisplay(BaseModel):
    title:str

class UserBase(BaseModel):
  username: str='User'
  email: str='user@gmail.com'
  password: str

class UserDisplay(BaseModel):
  username: str
  email: str
  class Config():
    orm_mode = True