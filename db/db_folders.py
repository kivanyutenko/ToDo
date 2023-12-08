from sqlalchemy.orm.session import Session
from db.models import DbFolder
from fastapi import HTTPException,status

def create_folder(db:Session,folder_name:str):
    new_folder=DbFolder(
        title=folder_name,
    )
    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)
    return new_folder


def get_all_folders(db:Session):
    return db.query(DbFolder).all()

def get_folder(db:Session,id:int):
    folder=db.query(DbFolder).filter(DbFolder.id==id).first()
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {id} not found')  
    return folder

def update_folder(db:Session,id:int,request:str):
    folder=db.query(DbFolder).filter(DbFolder.id==id)
    if not folder.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {id} not found')
    folder.update({
     DbFolder.title:request.title,
    })
    db.commit()
    return 'Success'

def delete_folder(db:Session,id:int):
    folder=db.query(DbFolder).filter(DbFolder.id==id).first()
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {id} not found')  
    db.delete(folder)
    db.commit()
    return 'Success'