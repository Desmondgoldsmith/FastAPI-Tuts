from fastapi import FastAPI, Response,status, HTTPException
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row

app = FastAPI()

class validatePosts(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int] = None
    
try:
    conn = psycopg.connect(host = 'localhost',database = 'fastapi',user = 'postgres',password = 'DessyAdmin07', cursor_factory=dict_row)
    cursor = conn.cursor()
    print("Database connection successfull")
except Exception as error:
    print(f"An error Occured:{error}")

all_posts = [
    {
        "id": 1,
        "title": "Forbes Update",
        "content": "Dessy is the World Richest Man!",
        "rating": 5
    },
    {
        "id": 2,
        "title": "News Updates",
        "content": "Dessy bought a private Jet worth $50m!",
        "rating": 5
    }
]


# function to search post by id
def SearchPost(id):
    for p in all_posts:
        if p['id'] == id:
            return p
        
# function to get the index of a post
def findIndex(id):
    for i,p in enumerate(all_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"Message: Hello world!"}

@app.get("/posts")
def posts():
    return {
            "status":"all posts retrieved successfully!",
            "body": all_posts,
           }

# create a post
@app.post("/create-post", status_code=status.HTTP_201_CREATED)
def create_post(posts:validatePosts):
    post_dict = posts.model_dump()
    post_dict['id'] = randrange(1,1000000000)
    all_posts.append(post_dict)
    return {
            "status":"post created successfully",
            "data": post_dict
           }

# retrieve one post
@app.get('/post/{id}')
def get_one_post(id:int, response:Response):
    find_post = SearchPost(id) 
    if not find_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found"}    
    print(find_post)
    return {
           "status": "Post retrieved successfully",
           "body": find_post
           } 
    
# delete a post
@app.delete('/delete_post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id:int):
    index = findIndex(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    
    all_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# update a post
@app.put('/update_post/{id}', status_code=status.HTTP_201_CREATED)
def updatePost(id:int, posts:validatePosts):
    index = findIndex(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    post_dict = posts.model_dump()
    post_dict['id'] = id
    all_posts[index] = post_dict
    return {
            "status":"Post Updated Successfully",
            "body": post_dict  
          }