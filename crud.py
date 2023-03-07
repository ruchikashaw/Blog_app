from sqlalchemy.orm import Session

import models,schema


def get_blog(db: Session, blog_id: int):
    return db.query(models.Blogs).filter(models.Blogs.id == blog_id).first()

def get_blogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Blogs).offset(skip).limit(limit).all()

def create_blog(db: Session, blog: schema.BlogCreate):
    db_blog = models.Blog(title=blog.title, description=blog.description)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


