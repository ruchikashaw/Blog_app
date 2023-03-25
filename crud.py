from sqlalchemy.orm import Session
from fastapi import HTTPException
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

def update_blog(db:Session, blog: schema.BlogUpdate, id:int):
        blog_update = db.query(models.Blogs).filter(models.Blogs.id == blog.id).first()
        if blog_update.owner_id==id:
            if blog.title:
                blog_update.title=blog.title
            db.add(blog_update)
            db.commit()
            db.refresh(blog_update)
        else:
            raise HTTPException(status_code=404, detail="You are not the owner of the blog")
        return blog_update

def delete_blog(db:Session, blog:schema.BlogDelete, id:int):
    deleted_blog = db.query(models.Blogs).filter(models.Blogs.id == blog.del_id).first()
    if deleted_blog.owner_id==id:
        db.delete(deleted_blog)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="You are not the owner of the blog")
    return deleted_blog

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
   blog = db.query(models.Blogs).filter(models.Blogs.id == comment.blog_id).first()
   if blog is None:
         raise HTTPException(status_code=404, detail="Blog not found")
   comments = models.Comments(message=comment.message,blog_id=comment.blog_id,owner_id=id)
   db.add(comments)
   db.commit()
   db.refresh(comments)
   return schema.Comment(message=comments.message, blog_id=comments.blog_id, owner_id=id)

def get_comments_by_blog_id(id:int,db:Session,skip:int=0,limit:int=100):
    return db.query(models.Comments).filter(models.Comments.blog_id==id).offset(skip).limit(limit).all()

def get_comments_by_user_id(user:int,db:Session,skip:int=0,limit:int=100):
    return db.query(models.Comments).filter(models.Comments.owner_id==user).offset(skip).limit(limit).all()

def create_upvote(upvotes:schema.Upvotecreate, user:int,db:Session):
    blog = db.query(models.Blogs).filter(models.Blogs.id == upvotes.blog_id).first()
    if blog is None:
         raise HTTPException(status_code=404, detail="Blog not found")
    db_upvote=db.query(models.blogUpvote).filter(models.blogUpvote.owner_id==user,models.blogUpvote.blog_id==blog.id).first()
    if db_upvote is None:
        dbs_upvote=models.blogUpvote(upvote=upvotes.upvote,blog_id=upvotes.blog_id,owner_id=user)
        db.add(dbs_upvote)
        db.commit()
        db.refresh(dbs_upvote)
    else:
        if upvotes.upvote and upvotes.downvote:
            raise HTTPException(status_code=404, detail="Downvote and Upvote cannot be same together")
        db_upvote.upvote=upvotes.upvote
        db_upvote.downvote=upvotes.downvote
        db.add(db_upvote)
        db.commit()
        db.refresh(db_upvote)
        
    return schema.blogupvote(upvote=db_upvote.upvote,downvote=db_upvote.downvote,blog_id=db_upvote.blog_id, owner_id=user)

def create_bookmark(bookmarks:schema.bookmarkbase, user: int, db:Session):
    blog = db.query(models.Blogs).filter(models.Blogs.id==bookmarks.blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    db_bookmark = db.query(models.Bookmark).filter(models.Bookmark.owner_id==user, models.Bookmark.blog_id==blog.id).first()
    if db_bookmark is None:
        db_bookmark = models.Bookmark(Bookmark=bookmarks.Bookmark, owner_id=user, blog_id=bookmarks.blog_id)
        db.add(db_bookmark)
        db.commit()
        db.refresh(db_bookmark)
        print(db_bookmark)
    else:
        db_bookmark.Bookmark=bookmarks.Bookmark
        db.add(db_bookmark)
        db.commit()
        db.refresh(db_bookmark)

    return schema.bookmarkCreate(Bookmark=db_bookmark.Bookmark,blog_id=db_bookmark.blog_id, owner_id=user)