from datetime import date, datetime, time
from fastapi import APIRouter, Depends,Query
from db.models import DbUser
from schemas import TaskBase, TaskDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_tasks
from typing import List
from auth.oauth2 import get_current_user, oauth2_scheme

router=APIRouter( prefix='/tasks',
                 tags=['tasks'])

#Create task
@router.post('/',response_model=TaskDisplay)
def create_task(request: TaskBase,
                db: Session=Depends(get_db),
                priority: str = Query("Normal", enum=['Low', 'Normal', 'High','Critical']),
                current_user: DbUser = Depends(get_current_user)):
    return db_tasks.create_task(db,request,priority,current_user)

#Read all tasks
@router.get('/',response_model=List[TaskDisplay])
def get_all_tasks(db:Session=Depends(get_db),current_user: DbUser = Depends(get_current_user)): #, token: str = Depends(oauth2_scheme)
    return db_tasks.get_all_tasks(db,current_user)

#Read one task
@router.get('/{id}',response_model=TaskDisplay)
def get_task(id:int,db:Session=Depends(get_db),current_user: DbUser = Depends(get_current_user)):
    return db_tasks.get_task(db,id,current_user)


#Update tasks
@router.put('/{id}')
def update_task(id:int,
                request:TaskBase,
                db:Session=Depends(get_db),
                status: str = Query('New', enum=['New', 'In progress', 'Done']),
                priority: str = Query('Normal', enum=['Low', 'Normal', 'High','Critical']),
                folder_id:int=Query("1"),
                flag:bool=Query(False,enum=[False,True]), 
                current_user: DbUser = Depends(get_current_user),
                date: str = Query(..., alias="dd.mm.yyyy"),
                time:str=Query(...,alias="hh:mm")
):
    date_iso = datetime.strptime(date, "%d.%m.%Y").date()
    time_iso = datetime.strptime(time, "%H:%M").time()
    return db_tasks.update_task(id,request,db,status,priority,flag,date_iso,time_iso,folder_id,current_user)

@router.delete('/{id}')
def delete_task(id:int=None, db: Session = Depends(get_db),delete_all:bool=Query(...,enum=[False,True]),current_user: DbUser = Depends(get_current_user)):
    if delete_all:
        return db_tasks.delete_all_tasks(db, current_user)
    else:
        return db_tasks.delete_task(db, id, current_user)


