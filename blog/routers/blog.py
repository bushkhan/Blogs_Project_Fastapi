from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .. import schemas, database
from .. import models
from sqlalchemy.orm import Session
from ..database import get_db
from ..repository import blog

router = APIRouter(prefix="/blog", tags=["blogs"])



#GET ALL BLOGS
@router.get("/", response_model=List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    return blog.get_all_blog(db)




#CREATE BLOG
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create_blog(request, db)




#GET SINGLE BLOG
@router.get("/{id}", status_code=200, response_model=schemas.ShowBlog)
def get_single_blog(id: int, db: Session = Depends(get_db)):
    return blog.get_single_blog(id,db)



#DELETE BLOG
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    return blog.delete_blog(id, db)




#UPDATE BLOG
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return update_blog(id, db,request)