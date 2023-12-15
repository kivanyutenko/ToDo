from fastapi import APIRouter, Depends,Query
from db.models import DbUser
from schemas import TaskBase, TaskDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_tasks
from typing import List, Optional
from auth.oauth2 import get_current_user, oauth2_scheme

router=APIRouter( prefix='/task',
                 tags=['task'])

#Create task
@router.post('/new',response_model=TaskDisplay)
def create_task(request: TaskBase,
                db: Session=Depends(get_db),
                priority: str = Query("Normal", enum=['Low', 'Normal', 'High','Critical']), token: str = Depends(oauth2_scheme),
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
@router.put('/{id}')
def update_task(id:int,
                request:TaskBase,
                db:Session=Depends(get_db),
                status: str = Query('New', enum=['New', 'In progress', 'Done']),
                priority: str = Query('Normal', enum=['Low', 'Normal', 'High','Critical']),
                folder_id:int=Query("1"), 
                token: str = Depends(oauth2_scheme),
                current_user: DbUser = Depends(get_current_user)):
    return db_tasks.update_task(id,request,db,status,priority,folder_id,current_user)

@router.delete('/{id}')
def delete_task(id:int=None, db: Session = Depends(get_db),delete_all:bool=Query(...,enum=[False,True]), token: str = Depends(oauth2_scheme), current_user: DbUser = Depends(get_current_user)):
    if delete_all:
        return db_tasks.delete_all_tasks(db, current_user)
    else:
        return db_tasks.delete_task(db, id, current_user)


