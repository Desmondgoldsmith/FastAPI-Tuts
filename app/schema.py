from pydantic import BaseModel
from datetime import datetime

class validatePosts(BaseModel):
    title: str
    content: str
    published: bool
    
    
class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime 
    
    class config:
        orm_model = True