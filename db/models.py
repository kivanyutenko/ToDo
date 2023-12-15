from db.database import Base
from sqlalchemy import Boolean, Column,Date,Time,DateTime
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class DbTask(Base):
    __tablename__='tasks'
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String,index=True)
    description=Column(String)
    task_status=Column(String)
    priority=Column(String)
    flag=Column(Boolean)
    date=Column(Date)
    time=Column(Time)
    folder_id=Column(Integer, ForeignKey("folders.id", ondelete='CASCADE'))
    folder=relationship("DbFolder", back_populates="tasks", foreign_keys=[folder_id])
    user_id=Column(Integer, ForeignKey("users.id", ondelete='CASCADE')) 
    user = relationship("DbUser", back_populates='items',foreign_keys=[user_id])

class DbFolder(Base):
    __tablename__='folders'
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String,index=True)
    tasks = relationship("DbTask", back_populates="folder", foreign_keys=[DbTask.folder_id])

class DbUser(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String )
  email = Column(String)
  password = Column(String)
  items = relationship('DbTask', back_populates='user', foreign_keys=[DbTask.user_id])