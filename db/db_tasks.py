from sqlalchemy.orm.session import Session
from db.models import DbFolder, DbTask, DbUser, DbTag 
from schemas import TaskBase
from fastapi import  HTTPException, status
from db.database import SessionLocal


#Creating new task. By default it's status is 'New' and folder is 'Main'
def create_task(db:Session,request:TaskBase,status,option,folder_id,flag,date_iso,time_iso,current_user,out_image_url, app_tag):
    folder=db.query(DbFolder).filter(DbFolder.id==folder_id).first()
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {folder_id} not found')
    if folder.user_id is not None and current_user.id != folder.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to place task in this folder') 
    
    selected_tags = []
    if app_tag:
        # Check for existing tags
        existing_tags = db.query(DbTag).filter(DbTag.name.in_(app_tag)).all()
        existing_tag_names = {tag.name for tag in existing_tags}

        # Create new tags if they don't exist
        for tag_name in app_tag:
            if tag_name not in existing_tag_names:
                new_tag = DbTag(name=tag_name, user_id=current_user.id)
                db.add(new_tag)
                db.commit()
                db.refresh(new_tag)
                selected_tags.append(new_tag)
            else:
                selected_tags.extend([tag for tag in existing_tags if tag.name == tag_name])
    
    
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
        app_tags=selected_tags
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
    if current_user.id != task.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to read this task')  
    return task

#Update  task
def update_task(id: int, request: TaskBase, db: Session, Status: str, priority: str, flag: bool, date_iso, time_iso, folder_id: int, current_user, image_url, app_tag):
    task = db.query(DbTask).filter(DbTask.id == id).first()
    folder = db.query(DbFolder).filter(DbFolder.id == folder_id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found')
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {folder_id} not found')
    if current_user.id != task.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to update this task')
    if folder.user_id is not None and current_user.id != folder.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to place task in this folder')

    selected_tags = []
    if app_tag:
        existing_tags = db.query(DbTag).filter(DbTag.name.in_(app_tag)).all()
        existing_tag_names = {tag.name for tag in existing_tags}

        for tag_name in app_tag:
            if tag_name not in existing_tag_names:
                new_tag = DbTag(name=tag_name, user_id=current_user.id)
                db.add(new_tag)
                db.commit()
                db.refresh(new_tag)
                selected_tags.append(new_tag)
            else:
                selected_tags.extend([tag for tag in existing_tags if tag.name == tag_name])

    task.title = request.title
    task.description = request.description
    task.task_status = Status
    task.priority = priority
    task.flag = flag
    task.folder_id = folder_id
    task.date = date_iso
    task.time = time_iso
    task.image_url = image_url
    task.app_tags = selected_tags  # Set the app_tags relationship directly

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

# Create a new tag
def create_app_tag(name: str,db,current_user):
    new_app_tag = DbTag(name=name, user_id=current_user.id)
    db.add(new_app_tag)
    db.commit()
    db.refresh(new_app_tag)
    return new_app_tag

# Get all tags
def get_all_app_tags(db,current_user):
    app_tags = db.query(DbTag).filter(DbTag.user_id==current_user.id).all()
    return app_tags

# Get tag by ID
def get_app_tag_by_id(app_tag_id: int,db,current_user):
    tag=db.query(DbTag).filter(DbTag.id==app_tag_id).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Tag with id {id} not found') 
    if current_user.id != tag.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to get this tag') 
    app_tag = db.query(DbTag).filter(DbTag.id == app_tag_id).first()
    return app_tag

# Update tag by ID
def update_app_tag(app_tag_id: int, new_name: str,db,current_user):
    app_tag = db.query(DbTag).filter(DbTag.id == app_tag_id).first()
    if not app_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Tag with id {id} not found') 
    if current_user.id != app_tag.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to update this tag') 
    if app_tag:
        app_tag.name = new_name
        db.commit()
        db.refresh(app_tag)
    return app_tag

# Delete tag by ID
def delete_app_tag(app_tag_id: int,db,current_user):
    app_tag = db.query(DbTag).filter(DbTag.id == app_tag_id).first()
    if not app_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Tag with id {id} not found') 
    if current_user.id != app_tag.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to delete this tag') 
    if app_tag:
        db.delete(app_tag)
        db.commit()
    return app_tag
