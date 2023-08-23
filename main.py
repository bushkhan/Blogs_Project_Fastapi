from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
app = FastAPI() #instace


# @app.get('/') 
#@app - path operation decorator
#get - operation
#/ - path
#path operation fucntion
#performing some operation on this path
# def index():
#     return {'data':'blog list'}


@app.get('/blog')
################# QUERY PARAMETER ################
#passing the parameters with datatypes also   
#default values can be given too
#optional values can be given too
def index(limit=10, published: bool = True, sort: Optional[str]= None):
    if published:
        return {"data":f"{limit} published blogs from db"}
    else:
        return {"data":f"{limit} non-published blogs from db"}
        
        
        
@app.get('/blog/unpublished') 
def unpublished():
    return {'data':'unpublished blogs'}


################# PATH PARAMETER ################
#data type passed using pydantic library
@app.get('/blog/{id}')
def about(id: int):
    #fecthing blog with id = id
    return {'data':id}


@app.get('/blog/{id}/comments')
def comments(id: int):
    return {'data':{'1','2'}}
   

class Blog(BaseModel):  
    title: str
    body: str
    published:Optional[bool]


@app.post('/blog')
def create_blog(blog: Blog):
    return {
        "blog":{
            "title":f'{blog.title}',
            "description":f'{blog.body}',
            "published":f'{blog.published}'
        }
    }