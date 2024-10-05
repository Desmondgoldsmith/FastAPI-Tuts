from fastapi import FastAPI, Response,status, HTTPException, Depends
import psycopg
from psycopg.rows import dict_row
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schema, utils
from typing import List
import time

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
    
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


# function to search post by id
# def SearchPost(id):
#     for p in all_posts:
#         if p['id'] == id:
#             return p
        
# function to get the index of a post
# def findIndex(id):
#     for i,p in enumerate(all_posts):
#         if p['id'] == id:
#             return i

@app.get("/")
async def root():
    return {"Message: Hello world!"}



# add a user
@app.post('/create_user', status_code=status.HTTP_201_CREATED, response_model=schema.UsersResponse)
def addUser(users:schema.UserSchema, db: Session = Depends(get_db)):
    # hash user password
    password_hash = utils.Hash(users.password)
    users.password = password_hash
    
    user_data = models.Users(**users.model_dump())
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


# get user
@app.get('/user/{id}', response_model= schema.UsersResponse)
def getUser(id:int, db:Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    
    return user