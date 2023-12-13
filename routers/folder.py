from typing import List
from fastapi import APIRouter,Depends
from db import db_folders
from sqlalchemy.orm import Session
from db.database import get_db

router=APIRouter( prefix='/folder',
                 tags=['folder'])
#Create folder
@router.post('/create_folder')
def create_folder(Folder_name:str,db:Session=Depends(get_db)):
    return db_folders.create_folder(db,Folder_name)

#Get all folders
@router.get('/all')
def get_all_folders(db:Session=Depends(get_db)):
    return db_folders.get_all_folders(db)

#Get folder
@router.get('/{id}')
def get_folder(folder_id:int,db:Session=Depends(get_db)):
    return db_folders.get_folder(db,folder_id)

#Update name of folder
@router.put('/{id}/update')
def update_folder(id:int,Folder_name:str,db:Session=Depends(get_db)):
    return db_folders.update_folder(db,id,Folder_name)

#Delete folder
@router.delete('/{id}/delete')
def delete_folder(id:int,db:Session=Depends(get_db)):
    return db_folders.delete_folder(db,id)