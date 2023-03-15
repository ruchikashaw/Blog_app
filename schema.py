from typing import Union
from pydantic import BaseModel

class Blogbase(BaseModel):
    title: str
    description: Union[str,None] = None

class BlogCreate(Blogbase):
    pass

class BlogDelete(BaseModel):
    del_id: int

class BlogUpdate(Blogbase):
    id:int

class BlogResponse(BaseModel):
    deleted_id:int

class datablog(BaseModel):
    title:str
    description:str

class BlogCreateresponse(BaseModel):
    id:int
    data:datablog
    
class Blog(Blogbase):
    id: int

    class Config:
        orm_mode = True

