from pydantic import BaseModel

class validatePosts(BaseModel):
    title: str
    content: str
    published: bool