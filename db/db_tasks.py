from sqlalchemy.orm.session import Session
from db.models import DbFolder, DbTask
from schemas import TaskBase
from fastapi import HTTPException,status

#Creating new task. By default it's status is 'New' and folder is 'Main'
def create_task(db:Session,request:TaskBase,option):
    new_task=DbTask(
        title=request.title,
        description=request.description,
        task_status='New',
        priority=option,
        folder_id=1
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


#Read all tasks
def get_all_tasks(db:Session):
    return db.query(DbTask).all()


#Read task
def get_task(db:Session,id:int):
    task=db.query(DbTask).filter(DbTask.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found')  
    return task

#Update title and description of task
def update_task(db:Session,id:int,request:TaskBase):
    task=db.query(DbTask).filter(DbTask.id==id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found')
    task.update({
     DbTask.title:request.title,
     DbTask.description:request.description
    })
    db.commit()
    return 'Success'

#Update status of task
def update_status_task(db:Session,id:int,request:str):
    task=db.query(DbTask).filter(DbTask.id==id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found')  
    task.update({
     DbTask.task_status:request,
    })
    db.commit()
    return 'Success'

#Update the priority of task
def update_priority_task(db:Session,id:int,request:str):
    task=db.query(DbTask).filter(DbTask.id==id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found')  
    task.update({
     DbTask.priority:request,
    })
    db.commit()
    return 'Success'

#Place task in other folder
def update_folder_task(db:Session,id:int,request:str):
    task=db.query(DbTask).filter(DbTask.id==id)
    folder=db.query(DbFolder).filter(DbFolder.id==request)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found') 
    if not folder.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {request} not found')  
    task.update({
     DbTask.folder_id:request,
    })
    db.commit()
    return 'Success'

#Delete task
def delete_task(db:Session,id:int):
    task=db.query(DbTask).filter(DbTask.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found')  
    db.delete(task)
    db.commit()
    return 'Success'