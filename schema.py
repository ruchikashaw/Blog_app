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
    id:int
    owner_id:int

    class Config:
        orm_mode = True

class Userbase(BaseModel):
    name: str
    email:str

class Usercreate(Userbase):
    password:str
    
class UserloginRequest(BaseModel):
    email:str
    password:str

class UserloginResponse(BaseModel):
    name:str
    token:str

class User(Userbase):
    id: int
    
    class Config:
        orm_mode=True

class CommentBase(BaseModel):
    message: str

class CommentCreate(CommentBase):
    blog_id:int

class CommentCreateResponse(CommentBase):
    blog_id:int

class Comment(CommentBase):
    blog_id:int
    owner_id:int

    class config:
        orm_mode:True