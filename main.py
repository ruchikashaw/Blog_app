from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schema
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/blogs/", response_model=schema.Blog)
def read_blogs(skip:int =0, limit:int = 100, db: Session = Depends(get_db)):
    blogs = crud.get_blogs(db,skip=skip,limit=limit)
    return blogs

@app.get("blogs/{id}", response_model=schema.Blog)
def read_blogs(id:int, db : Session=Depends(get_db)):
    db_blog = crud.get_blog(db,id=id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return db_blog

@app.post("/blogs/", response_model=schema.Blog)
def create_blog(blog: schema.BlogCreate, db: Session = Depends(get_db)):
    return crud.create_blog(db, title=blog.title, description=blog.description)










