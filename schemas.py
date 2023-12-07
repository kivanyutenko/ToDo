from pydantic import BaseModel

class TaskBase(BaseModel):
    title:str
    description:str
   # status:str

class TaskDisplay(BaseModel):
    title:str
    description:str
    status:str    