from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row
from .database import engine
from . import models
from .routers import posts,users,auth
import time

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
    
connection_successful = False

while not connection_successful:
    try:
        conn = psycopg.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
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

# post endpoint routes
app.include_router(posts.router)

# user endpoint routes
app.include_router(users.router)

# auth endpoint routes
app.include_router(auth.router)


