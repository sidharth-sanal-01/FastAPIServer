from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

# creating App instance for using FastAPI
app = FastAPI()


# API welcome message
@app.get("/test")
async def root(db: Session = Depends(get_db)):
    return {"Message": "Success"}


# from here it will check each route for a match and sends response based on that

# posts route
app.include_router(posts.router)
# user route
app.include_router(users.router)
# login route
app.include_router(auth.router)
