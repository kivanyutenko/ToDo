from db.database import Base
from sqlalchemy import Column #,func,DateTime
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
    folder_id=Column(Integer, ForeignKey("folders.id", ondelete='CASCADE'))
    folder=relationship("DbFolder", back_populates="tasks")
   # due_date = Column(DateTime(timezone=True), default=func.now())

    
class DbFolder(Base):
    __tablename__='folders'
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String,index=True)
    tasks = relationship("DbTask", back_populates="folder")

