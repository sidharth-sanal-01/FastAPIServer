from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session #session for connecting to database
from sqlalchemy import and_,or_ #to filter databsae based on mutliple queries 
from ..database import get_db  # we use this inside our dependency injection with in each request
from .. import models, schemas, oauth2


# creating a router for routing to post route
router = APIRouter(prefix="/posts", tags=["posts"])


# get all posts
@router.get("/", response_model=List[schemas.PostResponse])
async def getAllPosts(
    db: Session = Depends(get_db),
    currentUser: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    search: Optional[str] = "",
    skip: int = 3,
):
    print(limit)
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)
    )  # return all the data frm posts
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
        owner_id=currentUser.id, **post.model_dump()
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
    # check id
    if post.first() == None:
        raise HTTPException(
            detail="Post Not found", status_code=status.HTTP_404_NOT_FOUND
        )
    if currentUser.id != post.first().owner_id:
        # check whether the post owner is current user
        raise HTTPException(
            detail="You can only delete your posts..",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    post.delete(synchronize_session=False)  # default configuration
    db.commit()
    return {"Message": f"Post with id {id} deleted"}


# edit a post
@router.put("/{id}", response_model=schemas.PutResponseTest)
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
    if post_query.first().owner_id != currentUser.id:
        raise HTTPException(
            detail="You can only delete your posts..",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


# to get all posts related to a user
@router.get("/user/all", response_model=List[schemas.PostResponse])
def getAllUserPosts(
    currentUser: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
    limit: int = 5,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post)
        .filter(
            and_(
                models.Post.owner_id == currentUser.id,
                models.Post.title.ilike(f"%{search}%"),
            )
        )
        .limit(limit) #limit the number of results we get
        .offset(skip) # offset means skip the first n number of results
        .all() 
    )
    if posts == None:
        return []

    return posts
