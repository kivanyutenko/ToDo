from sqlalchemy.orm.session import Session
from db.models import DbTask
from schemas import TaskBase
from fastapi import HTTPException,status

def create_task(db:Session,request:TaskBase):
    new_task=DbTask(
        title=request.title,
        description=request.description,
        status='new'
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_all_tasks(db:Session):
    return db.query(DbTask).all()

def get_task(db:Session,id:int):
    task=db.query(DbTask).filter(DbTask.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found')  
    return task

def update_task(db:Session,id:int,request:TaskBase):
    task=db.query(DbTask).filter(DbTask.id==id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found')  
    task.update({
     DbTask.title:request.title,
     DbTask.description:request.description,
     DbTask.status:request.status  
    })
    db.commit()
    return 'ok'

def delete_task(db:Session,id:int):
    task=db.query(DbTask).filter(DbTask.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found')  
    db.delete(task)
    db.commit()
    return 'ok'