from sqlalchemy import  Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String, nullable = False)
    description = Column(String, server_default = "нет описания")
    completed = Column(Boolean, server_default = 'true')
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))