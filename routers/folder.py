# from fastapi import APIRouter,Depends
# from db import db_folders
# from sqlalchemy.orm import Session
# from db.database import get_db



# router=APIRouter( prefix='/folder',
#                  tags=['folder'])

# List_of_folders=['Main']

# @router.post('/create_folder')
# def create_folder(Folder_name:str,db:Session=Depends(get_db)):
#     return db_folders.create_folder(db,Folder_name)

# @router.get('/all')
# def get_all_folders(db:Session=Depends(get_db)):
#     return db_folders.get_all_folders(db)

# @router.patch('/{id}/update')
# def update_folder(id:int,Folder_name:str,db:Session=Depends(get_db)):
#     return db_folders.update_folder(db,id,Folder_name)

# @router.delete('/{id}/delete')
# def delete_folder(id:int,db:Session=Depends(get_db)):
#     return db_folders.delete_folder(db,id)