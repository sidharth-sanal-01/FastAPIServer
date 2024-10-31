from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2

# creating a router for routing to post route
router = APIRouter(prefix="/posts", tags=["posts"])


# get all posts
@router.get("/", response_model=List[schemas.PostResponse])
async def getAllPosts(
    db: Session = Depends(get_db), currentUser: int = Depends(oauth2.get_current_user)
):
    posts = db.query(models.Post).all()  # return all the data frm posts
    return posts


# get single posts
@router.get("/{id}", response_model=schemas.PostResponse)
async def getSinglePosts(
    id: int,
    db: Session = Depends(get_db),
    currentUser: int = Depends(oauth2.get_current_user),
):
    post = (
        db.query(models.Post).filter(models.Post.id == id).first()
    )  # using the filter method to filter based on ID and first method to return first match
    if post == None:
        raise HTTPException(
            detail="Post Not found", status_code=status.HTTP_404_NOT_FOUND
        )
    return post


# create a post
@router.post("/", response_model=schemas.PostResponse)
async def createNewPost(
    post: schemas.Post,
    db: Session = Depends(get_db),
    currentUser: int = Depends(oauth2.get_current_user),
):
    newPost = models.Post(
        **post.model_dump()
    )  # Automatically unpack all the fields of dictioanary
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost


# delete a post
@router.delete("/{id}")
async def deletePost(
    id: int,
    db: Session = Depends(get_db),
    currentUser: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            detail="Post Not found", status_code=status.HTTP_404_NOT_FOUND
        )
    post.delete(synchronize_session=False)  # default configuration
    db.commit()
    return {"Message": f"Post with id {id} deleted"}


# edit a post
@router.put("/{id}",response_model=schemas.PutResponseTest)
def update_post(
    id: int,
    post: schemas.Post,
    db: Session = Depends(get_db),
    currentUser: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(
            detail="Post Not Found", status_code=status.HTTP_404_NOT_FOUND
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
