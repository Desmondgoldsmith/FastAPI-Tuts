from fastapi import FastAPI, Response,status, HTTPException, Depends
import psycopg
from psycopg.rows import dict_row
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schema
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

# ======== USING NORMAL SQL QUERIES TO GET ALL POSTS ========== 
# @app.get("/posts")
# def posts():
#      cursor.execute('SELECT * FROM public."Posts"')
#      all_Posts = cursor.fetchall()
#      return {
#             "status":"all posts retrieved successfully!",
#             "body": all_Posts,
#            }

# ======== USING AN ORM TO GET ALL POSTS ===============
@app.get("/posts")
def GetPosts(db:Session = Depends(get_db)):
    data = db.query(models.Posts).all()
    return {
             "status": "success!",
             "data": data
           }
    
# create a post
@app.post("/create-post", status_code=status.HTTP_201_CREATED)
def create_post(posts:schema.validatePosts, db:Session = Depends(get_db)):
    # ===== USING NOWMAL SQL STATEMENTS =====
    # cursor.execute('INSERT INTO public."Posts" (title,content) VALUES(%s,%s) RETURNING *', (posts.title, posts.content))
    # post_added = cursor.fetchone()
    # conn.commit()
    
    # ===== USING THE SQLAlchemy ORM =====
    # data = models.Posts(title = posts.title, content = posts.content, published = posts.published)
    data = models.Posts(**posts.model_dump())
    db.add(data)
    db.commit()
    db.refresh(data)
    return {
            "status":"post created successfully",
            "data": data
           }

# retrieve one post
@app.get('/post/{id}')
def get_one_post(id:int, response:Response, db: Session = Depends(get_db)):
    # cursor.execute('SELECT * FROM public."Posts" WHERE id = %s',(id,))
    # find_post = cursor.fetchone()
    
    find_post = db.query(models.Posts).filter(models.Posts.id == id).first()
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
def deletePost(id:int, db:Session = Depends(get_db)):
    # cursor.execute('DELETE FROM public."Posts" WHERE id = %s RETURNING *',(id,))
    # deleted = cursor.fetchone()  
    # conn.commit() 
    deleted = db.query(models.Posts).filter(models.Posts.id == id)
    if deleted.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    deleted.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# update a post
@app.put('/update_post/{id}', status_code=status.HTTP_201_CREATED)
def updatePost(id:int, posts:schema.validatePosts, db:Session = Depends(get_db)):
    # cursor.execute('UPDATE public."Posts" SET title = %s, content = %s WHERE id = %s RETURNING *', (posts.title,posts.content,id,))
    # updated_post =cursor.fetchone()
    # conn.commit()
    # Query the post
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()

    # Check if the post exists
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found")

    # Update the post
    post_query.update(posts.model_dump(), synchronize_session=False)
    db.commit()

    # Refresh the post to get the updated data
    db.refresh(post)

    return {
        "status": "Post Updated Successfully",
        "body": post
    }