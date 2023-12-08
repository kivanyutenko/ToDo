from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String,Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class DbTask(Base):
    __tablename__='tasks'
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String)
    description=Column(String)
    task_status=Column(String)
    priority=Column(String)
    folder=Column(String)

# class DbFolder(Base):
#     __tablename__='folders'
#     id=Column(Integer, primary_key=True, index=True)
#     title=Column(String)