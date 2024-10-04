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
        from_attributes = True
        
class UserSchema(BaseModel):
    email: str
    password: str
    
class UsersResponse(UserSchema):
    id: int
    created_at: datetime