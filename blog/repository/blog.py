from sqlalchemy.orm import Session
from .. import schemas, models

from fastapi import HTTPException,status

def get_all_blog(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create_blog(request: schemas.Blog, db: Session):
    new_blog = models.Blog(
    title=request.title,
    body=request.body,
    user_id=1
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete_blog(id:int, db: Session):
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


def update_blog(id:int,request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} not found",
        )
    blog.update(request.model_dump())
    db.commit()
    return "updated"


def get_single_blog(id:int,db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} does not exist",
        )
    return blog