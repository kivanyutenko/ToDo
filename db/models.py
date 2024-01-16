from db.database import Base
from sqlalchemy import Boolean, Column,Date,Time, Table
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

# Define an association table to create the many-to-many relationship
task_tag_association = Table(
    'task_tag_association',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('tag_id', Integer, ForeignKey('app_tags.id'))
)


class DbTag(Base):
    __tablename__ = 'app_tags'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id=Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    user = relationship("DbUser", back_populates='app_tags')
    tasks = relationship("DbTask", secondary=task_tag_association, back_populates="app_tags")

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
    image_url = Column(String, nullable=True)
    app_tags = relationship("DbTag", secondary=task_tag_association, back_populates="tasks")
    
class DbFolder(Base):
    __tablename__='folders'
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String,index=True)
    tasks = relationship("DbTask", back_populates="folder", foreign_keys=[DbTask.folder_id])
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('DbUser', back_populates='folders')

class DbUser(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String )
  email = Column(String)
  password = Column(String)
  items = relationship('DbTask', back_populates='user', foreign_keys=[DbTask.user_id])
  folders = relationship('DbFolder', back_populates='user', cascade='all, delete-orphan')
  app_tags = relationship('DbTag', back_populates='user', foreign_keys=[DbTag.user_id] )
