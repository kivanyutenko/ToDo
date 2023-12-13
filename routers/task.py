from fastapi import APIRouter, Depends,Query
from schemas import TaskBase, TaskDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_tasks,db_folders
from typing import List

router=APIRouter( prefix='/task',
                 tags=['task'])

#Create task
@router.post('/create',response_model=TaskDisplay)
def create_task(request: TaskBase,
                db: Session=Depends(get_db),
                priority: str = Query(..., enum=['Low', 'Normal', 'High','Critical'])):
               # deadline:str=Query(...,enum=['False','True'])):
    return db_tasks.create_task(db,request,priority)

#Read all tasks
@router.get('/all',response_model=List[TaskDisplay])
def get_all_tasks(db:Session=Depends(get_db)):
    return db_tasks.get_all_tasks(db)

#Read one task
@router.get('/{id}',response_model=TaskDisplay)
def get_task(id:int,db:Session=Depends(get_db)):
    return db_tasks.get_task(db,id)
#Update tasks
@router.put('/{id}/update')
def update_task(id:int,request:TaskBase,db:Session=Depends(get_db)):
    return db_tasks.update_task(db,id,request)

#Update status of task
@router.put("/{id}/choose_status")
def update_status(id:int,db:Session=Depends(get_db), status: str = Query(..., enum=['New', 'In progress', 'Done'])):
    return db_tasks.update_status_task(db,id,status)

#Update folder of task
@router.put("/{id}/change_folder")
def change_folder(id:int,db:Session=Depends(get_db), folder_id: str = Query(...)):
    return db_tasks.update_folder_task(db,id,folder_id)

#Update priority of task
@router.put("/{id}/priority")
def update_priority(id:int,db:Session=Depends(get_db), priority: str = Query(..., enum=['Low', 'Normal', 'High','Critical'])):
    return db_tasks.update_priority_task(db,id,priority)

#Delete user
@router.delete('/{id}/delete')
def delete_task(id:int,db:Session=Depends(get_db)):
    return db_tasks.delete_task(db,id)
