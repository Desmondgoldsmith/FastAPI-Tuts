from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class validatePosts(BaseModel):
    title: str
    content: str
    published: bool
    
    

        
class UserSchema(BaseModel):
    email: EmailStr
    password: str
    
class UsersResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    
    # converty response to dictionary
    class Config:
        from_attributes = True 
        
class Post(validatePosts):
    id: int
    ownerID: int
    created_at: datetime 
    user: UsersResponse
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
    
    
class VotesData(BaseModel):
    postId: int
    action: conint(le:int = 1)