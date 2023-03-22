from sqlalchemy.orm import Session

import models,schema


def get_blog(db: Session, blog_id: int):
    data = db.query(models.Blogs).filter(models.Blogs.id == blog_id).first()
    return schema.BlogCreateresponse(id=blog_id,data=schema.datablog(title=data.title,description=data.description))
    # return schema.BlogCreateresponse(id=blog_id, data={"title":data.title,"description":data.description})

def get_blogs(id:int,db:Session,skip: int = 0, limit: int = 100):
    return db.query(models.Blogs).filter(models.Blogs.owner_id == id).offset(skip).limit(limit).all()


def create_blog(db: Session, blog: schema.BlogCreate, id:int):
    db_blog = models.Blogs(title=blog.title, description=blog.description, owner_id=id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def update_blog(db:Session, blog: schema.BlogUpdate):
    blog_update = db.query(models.Blogs).filter(models.Blogs.id == blog.id).first()
    if blog.title:
        blog_update.title=blog.title
    db.add(blog_update)
    db.commit()
    db.refresh(blog_update)
    return blog_update

def delete_blog(db:Session, blog:schema.BlogDelete):
    deleted_blog = db.query(models.Blogs).filter(models.Blogs.id == blog.del_id).first()
    db.delete(deleted_blog)
    db.commit()
    return schema.BlogResponse(deleted_id=blog.del_id)

def create_user(db:Session, user:schema.Usercreate):
    db_user = models.Users(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db:Session, user:schema.UserloginRequest):
    db_user = db.query(models.Users).filter(models.Users.email==user.email).first()
    return db_user

def get_user(db:Session, skip: int=0, limit:int =0):
    return db.query(models.Users).offset(skip).limit(limit).all()

def create_comment(db:Session, comment:schema.CommentCreate,id:int):
   comments = models.Comments(message=comment.message,blog_id=comment.blog_id,owner_id=id)
   db.add(comments)
   db.commit()
   db.refresh(comments)
   return schema.Comment(message=comments.message, blog_id=comments.blog_id, owner_id=id)

def get_comments_by_blog_id(id:int,db:Session,skip:int=0,limit:int=100):
    return db.query(models.Comments).filter(models.Comments.blog_id==id).offset(skip).limit(limit).all()

def get_comments_by_user_id(user:int,db:Session,skip:int=0,limit:int=100):
    return db.query(models.Comments).filter(models.Comments.owner_id==user).offset(skip).limit(limit).all()
