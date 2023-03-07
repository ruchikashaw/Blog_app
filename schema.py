from typing import Union
from pydantic import BaseModel

class Blogbase(BaseModel):
    title: str
    description: Union[str,None] = None

class BlogCreate(Blogbase):
    pass

class Blog(Blogbase):
    id: int

    class Config:
        orm_mode = True