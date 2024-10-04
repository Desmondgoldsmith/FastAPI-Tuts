from pydantic import BaseModel
from datetime import datetime


class validatePosts(BaseModel):
    title: str
    content: str
    published: bool
    
    
class Post(validatePosts):
    id: int
    created_at: datetime 
    class Config:
        orm_mode = True
        
class Users(BaseModel):
    email: str
    password: str
    
class UsersResponse(Users):
    id: int
    created_at: datetime