from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship

from database import Base


class Blogs(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String,unique=True,index=True)
    description = Column(String,index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True)
    email = Column(String, index=True, unique=True)
    password = Column(String,index=True)


owner = relationship("Users", back_populates="blogs")
    
