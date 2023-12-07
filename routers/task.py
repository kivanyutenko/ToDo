from fastapi import APIRouter, Depends
from schemas import TaskBase, TaskDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_tasks
from typing import List
from db.models import DbTask


router=APIRouter( prefix='/task',
                 tags=['task'])

#Create task
@router.post('/create',response_model=TaskDisplay)
def create_task(request: TaskBase, db: Session=Depends(get_db)):
    return db_tasks.create_task(db,request)

#Read all tasks
@router.get('/all',response_model=List[TaskDisplay])
def get_all_tasks(db:Session=Depends(get_db)):
    return db_tasks.get_all_tasks(db)

#Read one task
@router.get('/{id}',response_model=TaskDisplay)
def get_task(id:int,db:Session=Depends(get_db)):
    return db_tasks.get_task(db,id)
#Update tasks
@router.patch('/{id}/update')
def update_task(id:int,request:TaskDisplay,db:Session=Depends(get_db)):
    return db_tasks.update_task(db,id,request)
#Delete user
@router.delete('/delete/{id}')
def delete_task(id:int,db:Session=Depends(get_db)):
    return db_tasks.delete_task(db,id)
