from sqlalchemy.orm.session import Session
from db.database import SessionLocal
from db.models import DbFolder, DbTask
from fastapi import HTTPException,status
from sqlalchemy.orm import joinedload
from sqlalchemy_utils import database_exists

#Adding 'Main' in table folders
db=SessionLocal()
if database_exists('sqlite:///./tasks_database.db'): 
    main_folder=db.query(DbFolder).filter(DbFolder.title=='Main').first()
    if main_folder is None:
        main_folder=DbFolder(title="Main")
        db.add(main_folder)
        db.commit()
        db.refresh(main_folder)
db.close()

#Create new folder
def create_folder(db:Session,folder_name:str):
    new_folder=DbFolder(
        title=folder_name,
    )
    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)
    return new_folder

#Read all folders and tasks
def get_all_folders(db:Session):
    folders_with_tasks = db.query(DbFolder).options(joinedload(DbFolder.tasks)).all()
    return {'folders': folders_with_tasks}

#Read specific folder and tasks from it
def get_folder(db:Session,id:int):
    folder=db.query(DbFolder).filter(DbFolder.id==id).first()
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {id} not found') 
    tasks=db.query(DbTask).filter(DbTask.folder_id==id).all() 
    return {'folder':folder,'tasks':tasks}

#Update name of the folder
def update_folder(db:Session,id:int,request:str):
    folder=db.query(DbFolder).filter(DbFolder.id==id)
    if not folder.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {id} not found')
    folder.update({
     DbFolder.title:request,
    })
    db.commit()
    return 'Success'

#Delete specific folder and replace it in table tasks to 'Main'
def delete_folder(db:Session,id:int):
    folder=db.query(DbFolder).filter(DbFolder.id==id).first()
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {id} not found')
    tasks = db.query(DbTask).filter(DbTask.folder_id == id).all()
    for task in tasks:
        task.folder_id = 1 
        db.commit()
    db.delete(folder)
    db.commit()
    return 'Success'

