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


@app.post("/blogs", response_model=schema.Blog)
def create_blog(blog: schema.BlogCreate, db: Session = Depends(get_db)):
    return crud.create_blog(db, blog)


@app.get("/blogs", response_model=list[schema.Blog])
def read_blogs(skip:int =0, limit:int = 100, db: Session = Depends(get_db)):
    blogs = crud.get_blogs(db=db,skip=skip,limit=limit)
    return blogs

@app.get("/blogs/{id}", response_model=schema.BlogCreateresponse)
def read_blogs(id:int, db : Session=Depends(get_db)):
    db_blog = crud.get_blog(db,id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return db_blog

@app.put("/blogs/{id}",response_model=schema.Blog)
def update_blog(blog: schema.BlogUpdate, db: Session=Depends(get_db)):
    return crud.update_blog(db,blog)

@app.delete("/blogs/{id}", response_model=schema.BlogResponse)
def delete_blog(blog: schema.BlogDelete,db:Session=Depends(get_db)):
    return crud.delete_blog(db,blog)
    





