from sqlalchemy import Boolean, Column, Integer, String


from database import Base


class Blogs(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String,unique=True,index=True)
    description = Column(String,index=True)

   