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
@router.post('/',response_model=TaskDisplay)
def create_task(request: TaskBase, db: Session=Depends(get_db)):
    return db_tasks.create_user(db,request)

#Read all tasks
@router.get('/',response_model=List[TaskDisplay])
def get_all_tasks(db:Session=Depends(get_db)):
    return db_tasks.get_all_users(db)

#Read one task
@router.get('/{id}',response_model=TaskDisplay)
def get_task(id:int,db:Session=Depends(get_db)):
    return db_tasks.get_user(db,id)
#Update tasks
@router.patch('/{id}/update')
def update_task(id:int,request:TaskBase,db:Session=Depends(get_db)):
    return db_tasks.update_user(db,id,request)
#Delete user
@router.delete('/delete/{id}')
def delete_task(id:int,db:Session=Depends(get_db)):
    return db_tasks.delete_user(db,id)
