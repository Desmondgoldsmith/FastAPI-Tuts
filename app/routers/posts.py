from fastapi import Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schema, oAuth
from typing import List



router = APIRouter(
    # this is how we can add a prefix in FastApi
    # prefix = "/posts",
    tags = ['Posts']
)

# ======== USING NORMAL SQL QUERIES TO GET ALL POSTS ========== 
# @router.get("/posts")
# def posts():
#      cursor.execute('SELECT * FROM public."Posts"')
#      all_Posts = cursor.fetchall()
#      return {
#             "status":"all posts retrieved successfully!",
#             "body": all_Posts,
#            }

# ======== USING AN ORM TO GET ALL POSTS ===============
# instead of making the route /posts , we use a / because we already set the prefix
@router.get("/posts", response_model=List[schema.Post])
def GetPosts(db:Session = Depends(get_db), user:int = Depends(oAuth.getCurrentUser)):
    data = db.query(models.Posts).all()
    # print(user.email)
    return data
    
    
# create a post
@router.post("/create-post", status_code=status.HTTP_201_CREATED, response_model = schema.Post)
def create_post(posts:schema.validatePosts, db:Session = Depends(get_db), 
                # to make sure users are loggedIn before they can create a post
                userID:int = Depends(oAuth.getCurrentUser)):
    
    # ===== USING NOWMAL SQL STATEMENTS =====
    # cursor.execute('INSERT INTO public."Posts" (title,content) VALUES(%s,%s) RETURNING *', (posts.title, posts.content))
    # post_added = cursor.fetchone()
    # conn.commit()
    
    # ===== USING THE SQLAlchemy ORM =====
    # data = models.Posts(title = posts.title, content = posts.content, published = posts.published)
    data = models.Posts(ownerID = userID.id, **posts.model_dump())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data
           

# retrieve one post
@router.get('/post/{id}', response_model = schema.Post)
def get_one_post(id:int, response:Response, db: Session = Depends(get_db), userID:int = Depends(oAuth.getCurrentUser)):
    # cursor.execute('SELECT * FROM public."Posts" WHERE id = %s',(id,))
    # find_post = cursor.fetchone()
    
    find_post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not find_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found"}    
    return find_post
            
    
# delete a post
@router.delete('/delete_post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id:int, db:Session = Depends(get_db), userID:int = Depends(oAuth.getCurrentUser)):
    # cursor.execute('DELETE FROM public."Posts" WHERE id = %s RETURNING *',(id,))
    # deleted = cursor.fetchone()  
    # conn.commit() 
    deleted_query = db.query(models.Posts).filter(models.Posts.id == id)
    deleted = deleted_query.first()
    if deleted.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    
    # allowing users to only delete posts which they created
    if deleted.ownerID != userID.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f" You are unauthorised to delete this post")
    
    deleted_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# update a post
@router.put('/update_post/{id}', status_code=status.HTTP_201_CREATED, response_model = schema.Post)
def updatePost(id:int, posts:schema.validatePosts, db:Session = Depends(get_db), userID:int = Depends(oAuth.getCurrentUser)):
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

    # allowing users to only update posts which they created
    if post.ownerID != userID.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f" You are unauthorised to update this post")
        
    # Update the post
    post_query.update(posts.model_dump(), synchronize_session=False)
    db.commit()

    # Refresh the post to get the updated data
    db.refresh(post)

    return post
