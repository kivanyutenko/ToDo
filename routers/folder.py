from typing import List
from fastapi import APIRouter,Depends
from db import db_folders
from sqlalchemy.orm import Session
from db.database import get_db
from auth.oauth2 import get_current_user, oauth2_scheme
from db.models import DbUser


router=APIRouter( prefix='/folders',
                 tags=['folders'])
#Create folder
@router.post('/')
def create_folder(Folder_name:str,db:Session=Depends(get_db),current_user:DbUser = Depends(get_current_user)):
    return db_folders.create_folder(db,Folder_name,current_user)

#Get all folders
@router.get('/')
def get_all_folders(db:Session=Depends(get_db),current_user:DbUser = Depends(get_current_user)):
    return db_folders.get_all_folders(db,current_user)

#Get folder
@router.get('/{id}')
def get_folder(folder_id:int,db:Session=Depends(get_db),current_user:DbUser = Depends(get_current_user)):
    return db_folders.get_folder(db,folder_id, current_user)

#Update name of folder
@router.put('/{id}')
def update_folder(id:int,Folder_name:str,db:Session=Depends(get_db), current_user:DbUser = Depends(get_current_user)):
    return db_folders.update_folder(db,id,Folder_name,current_user)

#Delete folder
@router.delete('/{id}')
def delete_folder(id:int,db:Session=Depends(get_db), current_user:DbUser = Depends(get_current_user)):
    return db_folders.delete_folder(db,id,current_user)