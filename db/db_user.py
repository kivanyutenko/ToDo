from db.database import SessionLocal
from db.db_tasks import delete_all_tasks
from db.hash import Hash
from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbFolder, DbUser
from fastapi import HTTPException, status
from sqlalchemy_utils import database_exists


def create_user(db: Session, request: UserBase):
  #Adding 'Main' in table folders
  if database_exists('sqlite:///./tasks_database.db'):
      db=SessionLocal()
      main_folder=db.query(DbFolder).filter(DbFolder.title=='Main').first()
      if main_folder is None:
          main_folder=DbFolder(title="Main")
          db.add(main_folder)
          db.commit()
          db.refresh(main_folder)
          db.close()
  new_user = DbUser(
    username = request.username,
    email = request.email,
    password = Hash.bcrypt(request.password)
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def get_all_users(db: Session):
  return db.query(DbUser).all()

def get_user(db: Session, id: int):
  user = db.query(DbUser).filter(DbUser.id == id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with id {id} not found')
  return user

def get_user_by_username(db: Session, username: str):
  user = db.query(DbUser).filter(DbUser.username == username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with username {username} not found')
  return user

def update_user(db: Session, id: int, request: UserBase,current_user):
  user = db.query(DbUser).filter(DbUser.id == id)
  if not user.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with id {id} not found')
  if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to update this user')
  user.update({
    DbUser.username: request.username,
    DbUser.email: request.email,
    DbUser.password: Hash.bcrypt(request.password)
  })
  db.commit()
  return 'Success'

def delete_user(db: Session, id: int,current_user):
  user = db.query(DbUser).filter(DbUser.id == id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with id {id} not found')
  if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to delete this user')
  delete_all_tasks(db, current_user)
  db.delete(user)
  db.commit()
  return 'Success'