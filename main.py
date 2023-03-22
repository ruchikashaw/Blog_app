from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
import crud, models, schema
from database import SessionLocal, engine
import time
import jwt
models.Base.metadata.create_all(bind=engine)
JWT_SECRET="hello"
JWT_ALGORITHM="HS256"
app = FastAPI()


def createToken(userId):
    payload = {
        "Id": userId,
        "expires": time.time() + 6000
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token

def decodeToken(token):
    try:
        decoded_token=jwt.decode(token,JWT_SECRET,JWT_ALGORITHM)
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        print(e)
        {}

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
        
    def verify_jwt(self,token):
        istokenValid: bool = False
        try:
            payload = decodeToken(token)
        except:
            payload = None
        if payload:
            istokenValid = True
        return istokenValid



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 


@app.post("/blogs", response_model=schema.Blog)
def create_blog(blog: schema.BlogCreate, token:str = Depends(JWTBearer()),db: Session = Depends(get_db)):
    user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    id = user["Id"]
    return crud.create_blog(db, blog, id)



@app.get("/blogs",dependencies=[Depends(JWTBearer())], response_model=list[schema.Blog])
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
    
@app.post("/signup", response_model=schema.User)
def create_user(user:schema.Usercreate,db:Session=Depends(get_db)):
    return crud.create_user(db,user)

@app.post("/login", response_model=schema.UserloginResponse)
def login_user(user:schema.UserloginRequest,db:Session=Depends(get_db)):
    db_user = crud.login_user(db,user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.password == user.password:
        return schema.UserloginResponse(name=db_user.name,token=createToken(db_user.id))
    else:
        raise HTTPException(status_code=401, detail="Invalid Password")

@app.get("/users",response_model=list[schema.User])
def get_users(skip:int =0, limit:int=100,db:Session=Depends(get_db)):
    users = crud.get_user(db=db,skip=skip,limit=limit)
    return users

