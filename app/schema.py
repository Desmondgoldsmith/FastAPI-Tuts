from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


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
    email: str
    created_at: datetime
    
    # converty response to dictionary
    class Config:
        from_attributes = True 
        
    
class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    type: str
    token: str
    

class TokenData(BaseModel):
    id: Optional[str] = None
    