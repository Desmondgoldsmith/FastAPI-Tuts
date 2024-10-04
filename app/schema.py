from pydantic import BaseModel, EmailStr
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
    email: EmailStr
    password: str
    
class UsersResponse(UserSchema):
    id: int
    created_at: datetime
    
    # converty response to dictionary
    class Config:
        from_attributes = True 