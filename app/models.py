from sqlalchemy import Columns, Integer, String, Boolean
from .database import Base


def Posts(Base):
    __tablename__ = 'posts'
    
    id = Columns(Integer, primary_key = True, nullable=False)
    title = Columns(String, nullable=False)
    content = Columns(String , nullable = False)
    published = Columns(Boolean, nullable=True)