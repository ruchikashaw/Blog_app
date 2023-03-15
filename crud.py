from sqlalchemy.orm import Session

import models,schema


def get_blog(db: Session, blog_id: int):
    data = db.query(models.Blogs).filter(models.Blogs.id == blog_id).first()
    return schema.BlogCreateresponse(id=blog_id,data=schema.datablog(title=data.title,description=data.description))
    # return schema.BlogCreateresponse(id=blog_id, data={"title":data.title,"description":data.description})
    
def get_blogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Blogs).offset(skip).limit(limit).all()

def create_blog(db: Session, blog: schema.BlogCreate):
    db_blog = models.Blogs(title=blog.title, description=blog.description)
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
