#from datetime import datetime
from pydantic import BaseModel

class TaskBase(BaseModel):
    title:str='Name the task'
    description:str='Something to do'

class TaskDisplay(BaseModel):
    title:str
    description:str
    task_status:str
    priority:str 
    folder_id:int 
    #due_date: datetime  

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