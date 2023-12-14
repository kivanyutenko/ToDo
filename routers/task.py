from fastapi import APIRouter, Depends,Query
from db.models import DbUser
from schemas import TaskBase, TaskDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_tasks
from typing import List
from auth.oauth2 import get_current_user, oauth2_scheme


router=APIRouter( prefix='/task',
                 tags=['task'])

#Create task
@router.post('/create',response_model=TaskDisplay)
def create_task(request: TaskBase,
                db: Session=Depends(get_db),
                priority: str = Query(..., enum=['Low', 'Normal', 'High','Critical']), token: str = Depends(oauth2_scheme),
                current_user: DbUser = Depends(get_current_user)):
               # deadline:str=Query(...,enum=['False','True'])):
    return db_tasks.create_task(db,request,priority,current_user)

#Read all tasks
@router.get('/all',response_model=List[TaskDisplay])
def get_all_tasks(db:Session=Depends(get_db), token: str = Depends(oauth2_scheme),current_user: DbUser = Depends(get_current_user)):
    return db_tasks.get_all_tasks(db,current_user)

#Read one task
@router.get('/{id}',response_model=TaskDisplay)
def get_task(id:int,db:Session=Depends(get_db), token: str = Depends(oauth2_scheme),current_user: DbUser = Depends(get_current_user)):
    return db_tasks.get_task(db,id,current_user)
#Update tasks
@router.put('/{id}/update')
def update_task(id:int,request:TaskBase,db:Session=Depends(get_db), token: str = Depends(oauth2_scheme),current_user: DbUser = Depends(get_current_user)):
    return db_tasks.update_task(db,id,request,current_user)

#Update status of task
@router.put("/{id}/choose_status")
def update_status(id:int,db:Session=Depends(get_db), status: str = Query(..., enum=['New', 'In progress', 'Done']), 
                  token: str = Depends(oauth2_scheme),current_user: DbUser = Depends(get_current_user)):
    return db_tasks.update_status_task(db,id,status,current_user)

#Update folder of task
@router.put("/{id}/change_folder")
def change_folder(id:int,db:Session=Depends(get_db), folder_id: str = Query(...), token: str = Depends(oauth2_scheme),current_user: DbUser = Depends(get_current_user)):
    return db_tasks.update_folder_task(db,id,folder_id,current_user)

#Update priority of task
@router.put("/{id}/priority")
def update_priority(id:int,db:Session=Depends(get_db), priority: str = Query(..., enum=['Low', 'Normal', 'High','Critical']), 
                    token: str = Depends(oauth2_scheme),current_user: DbUser = Depends(get_current_user)):
    return db_tasks.update_priority_task(db,id,priority,current_user)

#Delete task
@router.delete('/{id}/delete')
def delete_task(id:int,db:Session=Depends(get_db), token: str = Depends(oauth2_scheme),current_user: DbUser = Depends(get_current_user)):
    return db_tasks.delete_task(db,id,current_user)

#Delete all tasks
@router.delete('/delete_all')
def delete_all_tasks(db:Session=Depends(get_db), token: str = Depends(oauth2_scheme),current_user: DbUser = Depends(get_current_user)):
    return db_tasks.delete_tasks_for_user(db,current_user)
