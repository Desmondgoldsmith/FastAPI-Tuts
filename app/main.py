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



