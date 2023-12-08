from pydantic import BaseModel

class TaskBase(BaseModel):
    title:str
    description:str

class TaskDisplay(BaseModel):
    title:str
    description:str
    task_status:str
    priority:str 
    folder:str 

