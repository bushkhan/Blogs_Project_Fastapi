from fastapi import FastAPI, Depends, status, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post(
    "/blog",
    status_code=status.HTTP_201_CREATED,
    tags=['blogs']
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


  
@app.get("/blog", response_model=List[schemas.ShowBlog],  tags=['blogs'])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}",  tags=['blogs'], status_code=200, response_model=schemas.ShowBlog)
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
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f"Blog with the id {id} does not exist"}
    return blog


@app.delete(
    "/blog/{id}",  tags=['blogs'],
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


@app.put(
    "/blog/{id}",  tags=['blogs'],
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


@app.post("/user",  tags=['users'])
def create_user(
    request: schemas.User,
    db: Session = Depends(get_db),
):
    # hashed passowrd
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}",  tags=['users'], response_model=schemas.ShowUser)
def get_single_user(
    id: int,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    return user
