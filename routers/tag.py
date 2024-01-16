from fastapi import APIRouter, Depends, HTTPException
from db.models import DbUser
from schemas import TagDisplay, TaskDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_tasks
from typing import List
from auth.oauth2 import get_current_user


router=APIRouter(tags=['tags'])

# CRUD operations for Tags
@router.post('/app_tags/', response_model=TagDisplay)
def create_app_tag(name: str, db: Session = Depends(get_db),current_user: DbUser = Depends(get_current_user)):
    return db_tasks.create_app_tag(name,db,current_user)

@router.get('/app_tags/', response_model=List[TagDisplay])
def get_all_app_tags(db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    return db_tasks.get_all_app_tags(db,current_user)

@router.get('/app_tags/{id}', response_model=TagDisplay)
def get_app_tag_by_id(app_tag_id: int, db: Session = Depends(get_db),current_user: DbUser = Depends(get_current_user)):
    tag = db_tasks.get_app_tag_by_id(app_tag_id,db,current_user)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # Fetch tasks associated with the tag using the relationship
    tasks_associated_with_tag = tag.tasks  # Assuming 'tasks' is the relationship name
    
    # Create a list of task titles for associated tasks
    associated_task_titles = [task.title for task in tasks_associated_with_tag]
    
    # Create a TagDisplay object with the associated task titles
    tag_display = TagDisplay(
        id=tag.id,
        name=tag.name,
        associated_tasks=associated_task_titles
    )
    return tag_display

@router.put('/app_tags/{id}', response_model=TagDisplay)
def update_app_tag(app_tag_id: int, name: str, db: Session = Depends(get_db),current_user: DbUser = Depends(get_current_user)):
    return db_tasks.update_app_tag(app_tag_id, name,db,current_user)

@router.delete('/app_tags/{id}', response_model=TagDisplay)
def delete_app_tag(app_tag_id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    return db_tasks.delete_app_tag(app_tag_id,db,current_user)