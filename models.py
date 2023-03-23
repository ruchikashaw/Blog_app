from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship

from database import Base


class Blogs(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String,unique=True,index=True)
    description = Column(String,index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="blogs")

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True)
    email = Column(String, index=True, unique=True)
    password = Column(String,index=True)
    blogs = relationship("Blogs", back_populates="owner")
    comments = relationship("Comments", back_populates="owner")
    blog_upvote= relationship("blogUpvote", back_populates="owner")

class Comments(Base):
    __tablename__='comments'

    id=Column(Integer, primary_key=True, index=True)
    message=Column(String,index=True)
    blog_id=Column(Integer, ForeignKey("blogs.id"), index=True)
    owner_id=Column(Integer, ForeignKey("users.id"), index=True)
    owner = relationship("Users", back_populates="comments")

class blogUpvote(Base):
    __tablename__='blog_upvote'

    id=Column(Integer, primary_key=True, index = True)
    upvote=Column(Boolean, index=True)
    downvote=Column(Boolean, index=True)
    blog_id=Column(Integer,ForeignKey("blogs.id"), index=True)
    owner_id=Column(Integer, ForeignKey("users.id"), index=True)
    owner = relationship("Users", back_populates="blog_upvote")
