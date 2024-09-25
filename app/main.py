from fastapi import FastAPI, Response,status, HTTPException
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()

class validatePosts(BaseModel):
    title: str
    content: str
    

connection_successful = False

while not connection_successful:
    try:
        conn = psycopg.connect(
            host='localhost',
            dbname='FastAPI_DB',
            user='postgres',
            password='DessyAdmin',
            port='5432',
            row_factory=dict_row
        )
        cursor = conn.cursor()
        print("Database connection successful")
        connection_successful = True
    except Exception as error:
        print(f"An error occurred: {error}")
        print("Retrying in 2 seconds...")
        time.sleep(2)


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
     cursor.execute('SELECT * FROM public."Posts"')
     all_Posts = cursor.fetchall()
     return {
            "status":"all posts retrieved successfully!",
            "body": all_Posts,
           }

# create a post
@app.post("/create-post", status_code=status.HTTP_201_CREATED)
def create_post(posts:validatePosts):
    cursor.execute('INSERT INTO public."Posts" (title,content) VALUES(%s,%s) RETURNING *', (posts.title, posts.content))
    post_added = cursor.fetchone()
    conn.commit()
    return {
            "status":"post created successfully",
            "data": post_added
           }

# retrieve one post
@app.get('/post/{id}')
def get_one_post(id:int, response:Response):
    cursor.execute('SELECT * FROM public."Posts" WHERE id = %s',(id,))
    find_post = cursor.fetchone()
    if not find_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found"}    
    return {
           "status": "Post retrieved successfully",
           "body": find_post
           } 
    
# delete a post
@app.delete('/delete_post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id:int):
    cursor.execute('DELETE FROM public."Posts" WHERE id = %s RETURNING *',(id,))
    deleted = cursor.fetchone()  
    conn.commit() 
    if deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# update a post
@app.put('/update_post/{id}', status_code=status.HTTP_201_CREATED)
def updatePost(id:int, posts:validatePosts):
    cursor.execute('UPDATE public."Posts" SET title = %s, content = %s WHERE id = %s RETURNING *', (posts.title,posts.content,id,))
    updated_post =cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    return {
            "status":"Post Updated Successfully",
            "body": updated_post  
          }