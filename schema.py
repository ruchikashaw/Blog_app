from typing import Union
from pydantic import BaseModel

class Blogbase(BaseModel):
    title: str
    description: Union[str,None] = None

class BlogCreate(Blogbase):
    pass

class BlogDelete(BaseModel):
    id:int

class BlogUpdate(Blogbase):
    id:int

class BlogResponse(BaseModel):
    status:str

class Blog(Blogbase):
    id: int

    class Config:
        orm_mode = True

