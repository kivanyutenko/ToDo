from typing import List
from db.models import DbUser
from schemas import UserBase, UserDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from auth.oauth2 import get_current_user, oauth2_scheme

router = APIRouter(
  prefix='/user',
  tags=['user']
)

# Create user
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
  return db_user.create_user(db, request)

# Read all users
@router.get('/all', response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
  return db_user.get_all_users(db)

# Read one user
@router.get('/{id}', response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
  return db_user.get_user(db, id)

# Update user
@router.put('/{id}')
def update_user(id: int, request: UserBase, db: Session = Depends(get_db), 
                token: str = Depends(oauth2_scheme),current_user: DbUser = Depends(get_current_user)):
  return db_user.update_user(db, id, request,current_user)

# Delete user
@router.delete('/{id}')
def delete(id: int, db: Session = Depends(get_db), 
           token: str = Depends(oauth2_scheme),current_user: DbUser = Depends(get_current_user)):
  return db_user.delete_user(db, id,current_user)