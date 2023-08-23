from fastapi import APIRouter,Depends, HTTPException,status
from typing import List
from .. import schemas, database
from .. import models
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix='/blog',
    tags=['blogs']
    )


        
@router.get("/", response_model=List[schemas.ShowBlog],  )
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,

)
def create_blog(
    request: schemas.Blog,
    db: Session = Depends(get_db),
):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=1
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



@router.get("/{id}",  status_code=200, response_model=schemas.ShowBlog)
def get_single_blog(
    id: int,
    db: Session = Depends(
        get_db,
    ),
):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} does not exist",
        )
    return blog


@router.delete(
    "/{id}", 
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_blog(
    id: int,
    db: Session = Depends(get_db),
):
    blog = (
        db.query(models.Blog)
        .filter(models.Blog.id == id)
        .delete(synchronize_session=False)
    )
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="id does not exists!",
        )
    db.commit()
    return {"details": f"Blog with the id {id} deleted Successfully"}



@router.put(
    "/{id}", 
    status_code=status.HTTP_202_ACCEPTED,
)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} not found",
        )
    blog.update(request.model_dump())
    db.commit()
    return "updated"