from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class Posts(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key = True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String , nullable = False)
    published = Column(Boolean, server_default = 'True', nullable=False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = True , server_default =  text('now()')) 


class Users(Base):
    __tablename__= 'users'
    
    id = Column(Integer , nullable = False , primary_key = True)    
    email = Column(String , nullable = False, unique = True)
    password = Column(String , nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = True , server_default =  text('now()'))