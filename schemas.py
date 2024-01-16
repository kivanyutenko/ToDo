from datetime import date, time
from typing import Optional
from pydantic import BaseModel
from typing import Optional, List


class TaskDisplay(BaseModel):
    title:str
    description:str
    task_status:str
    priority:str
    flag:bool
    date:date
    time:time
    folder_id:int
    image_url: Optional[str] = None
    # app_tag: Optional[str] = None

    class Config:
      orm_mode = True
      json_encoders = {
            date: lambda v: v.strftime("%d.%m.%Y"),
            time: lambda v: v.strftime("%H:%M")
        }


class TagBase(BaseModel):
    name: str

class TagDisplay(BaseModel):
    id: int
    name: str
    associated_tasks: List[str] = []
  
class TaskBase(BaseModel):
    title:str='Task'
    description:str='Something to do'


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
