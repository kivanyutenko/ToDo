from sqlalchemy.orm.session import Session
from db.models import DbFolder, DbTask, DbUser
from schemas import TaskBase
from fastapi import  HTTPException, status

#Creating new task. By default it's status is 'New' and folder is 'Main'
def create_task(db:Session,request:TaskBase,status,option,folder_id,flag,date_iso,time_iso,current_user,out_image_url):
    folder=db.query(DbFolder).filter(DbFolder.id==folder_id).first()
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {folder_id} not found')
    if folder.user_id is not None and current_user.id != folder.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to place task in this folder') 
    new_task=DbTask(
        title=request.title,
        description=request.description,
        task_status=status,
        priority=option,
        date=date_iso,
        time=time_iso,
        flag=flag,
        folder_id=folder_id,
        user_id=current_user.id,
        image_url=out_image_url,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


#Read all tasks
def get_all_tasks(db:Session,current_user):
    return db.query(DbTask).filter(DbTask.user_id == current_user.id).all()


#Read task
def get_task(db:Session,id:int,current_user):
    task=db.query(DbTask).filter(DbTask.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found')
    if current_user.id != DbTask.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to read this task')  
    return task

#Update  task
def update_task(id:int,request:TaskBase,db:Session,Status:str,priority:str,flag:bool,date_iso,time_iso,folder_id:int,current_user,image_url):
    task=db.query(DbTask).filter(DbTask.id==id).first()
    folder=db.query(DbFolder).filter(DbFolder.id==folder_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found')
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {folder_id} not found') 
    if current_user.id != task.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to update this task')
    if folder.user_id is not None and current_user.id != folder.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to place task in this folder')
    db.query(DbTask).filter(DbTask.id == id).update({
        DbTask.title: request.title,
        DbTask.description: request.description,
        DbTask.task_status:Status,
        DbTask.priority:priority,
        DbTask.flag:flag,
        DbTask.folder_id:folder_id,
        DbTask.date:date_iso,
        DbTask.time:time_iso,
        DbTask.image_url:image_url,
    })
    db.commit()
    return 'Success'


#Delete task
def delete_task(db:Session,id:int, current_user):
    task=db.query(DbTask).filter(DbTask.id==id ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found') 
    if current_user.id != task.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to delete this task') 
    db.delete(task)
    db.commit()
    return 'Success'

def delete_all_tasks(db: Session, current_user):
    user = db.query(DbUser).filter(DbUser.id == current_user.id).first()
    if user:
        tasks_to_delete = db.query(DbTask).filter(DbTask.user_id == current_user.id).all()
        for task in tasks_to_delete:
            db.delete(task)
        db.commit()
        return 'Success'
