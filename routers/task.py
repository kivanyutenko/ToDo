from datetime import date, datetime, time
from fastapi import APIRouter, Depends,Query,UploadFile, File 
from db.models import DbUser
from schemas import TaskBase, TaskDisplay, TaskUpdate
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_tasks
from typing import List
from auth.oauth2 import get_current_user, oauth2_scheme
import random, string, shutil

router=APIRouter( prefix='/tasks',
                 tags=['tasks'])

image_url_types = ['absolute', 'relative']

#Create task
@router.post('/',response_model=TaskDisplay)
def create_task(request: TaskBase,
                db: Session=Depends(get_db),
                priority: str = Query("Normal", enum=['Low', 'Normal', 'High','Critical']),
                current_user: DbUser = Depends(get_current_user)):
    return db_tasks.create_task(db,request,priority,current_user)

#Upload image
@router.post('/image')
def upload_image(image: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
  letters = string.ascii_letters
  rand_str = ''.join(random.choice(letters) for i in range(6))
  new = f'_{rand_str}.'
  filename = new.join(image.filename.rsplit('.', 1))
  path = f'images/{filename}'

  with open(path, "w+b") as buffer:
    shutil.copyfileobj(image.file, buffer)
  
  return {'filename': path}

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
                time:str=Query(...,alias="hh:mm"),
                image_url:str=Query(None),
                image_url_type:str=Query(None,enum=image_url_types)
):
    date_iso = datetime.strptime(date, "%d.%m.%Y").date()
    time_iso = datetime.strptime(time, "%H:%M").time()
    return db_tasks.update_task(id,request,db,status,priority,flag,date_iso,time_iso,folder_id,current_user,image_url,image_url_type)

@router.delete('/{id}')
def delete_task(id:int=None, db: Session = Depends(get_db),delete_all:bool=Query(...,enum=[False,True]),current_user: DbUser = Depends(get_current_user)):
    if delete_all:
        return db_tasks.delete_all_tasks(db, current_user)
    else:
        return db_tasks.delete_task(db, id, current_user)


