from fastapi import FastAPI, Depends, status, HTTPException
from . import schemas, models
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash
from .routers import blog
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)



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
