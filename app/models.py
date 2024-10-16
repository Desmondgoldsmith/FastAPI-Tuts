from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
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
    ownerID = Column(Integer,ForeignKey('users.id', ondelete = "CASCADE"), nullable = False)

    user = relationship("Users")
    
class Users(Base):
    __tablename__= 'users'
    
    id = Column(Integer , nullable = False , primary_key = True)    
    email = Column(String , nullable = False, unique = True)
    password = Column(String , nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = True , server_default =  text('now()'))


class Votes(Base):
    __tablename__ = 'votes'
    
    postId = Column(Integer, ForeignKey('posts.id', ondelete = "CASCADE"), nullable = False, primary_key = True)
    userId = Column(Integer, ForeignKey('user.id', ondelete = "CASCADE"), nullable = False, primary_key = True)