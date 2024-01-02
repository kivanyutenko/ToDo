from sqlalchemy.orm.session import Session
from db.models import DbFolder, DbTask
from fastapi import HTTPException,status

#Create new folder
def create_folder(db:Session,folder_name:str,current_user):
    new_folder=DbFolder(
        title=folder_name,
        user_id=current_user.id
    )
    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)
    return new_folder

def get_all_folders(db:Session,current_user):
    folders=db.query(DbFolder).filter((DbFolder.user_id==current_user.id)|(DbFolder.user_id==None)).all()
    folders_with_tasks = [
        {
            'folder': folder,
            'tasks': db.query(DbTask).filter((DbTask.folder_id == folder.id)&(DbTask.user_id == current_user.id)).all()
        }
        for folder in folders
    ]
    return folders_with_tasks

#Read specific folder and tasks from it
def get_folder(db:Session,id:int,current_user):
    folder=db.query(DbFolder).filter(DbFolder.id==id).first()
    folder_user=db.query(DbFolder).filter((DbFolder.id==id)&((DbFolder.user_id==current_user.id)|(DbFolder.user_id==None))).first()
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {id} not found')
    if not folder_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to read this folder') 
    tasks=db.query(DbTask).filter((DbTask.folder_id==id) & (DbTask.user_id==current_user.id)).all() 
    return {'folder':folder,'tasks':tasks}

#Update name of the folder
def update_folder(db:Session,id:int,request:str,current_user):
    folder=db.query(DbFolder).filter(DbFolder.id==id)
    folder_user=db.query(DbFolder).filter((DbFolder.id==id)&(DbFolder.user_id==current_user.id)).first()
    if not folder.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {id} not found')
    if not folder_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to rename this folder') 
    folder.update({
     DbFolder.title:request,
    })
    db.commit()
    return 'Success'

#Delete specific folder and replace it in table tasks to 'Main'
def delete_folder(db:Session,id:int,current_user):
    folder=db.query(DbFolder).filter(DbFolder.id==id).first()
    folder_user=db.query(DbFolder).filter((DbFolder.id==id)&(DbFolder.user_id==current_user.id)).first()
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {id} not found')
    if not folder_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to delete this folder') 
    tasks = db.query(DbTask).filter((DbTask.folder_id == id)&(DbFolder.user_id==current_user.id)).all()
    for task in tasks:
        task.folder_id = 1 
        db.commit()
    db.delete(folder)
    db.commit()
    return 'Success'

