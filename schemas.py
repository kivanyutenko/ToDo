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
