

from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import true
from app import models, oauth2
from .. database import get_db
from sqlalchemy.orm import Session
from .. schemas import PostCreate, PostResponse, Postout
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# //////////////////////////////// POSTS ////////////////////////////////////////////////////////
@router.get("/", response_model=List[Postout])
def get_posts(db: Session = Depends(get_db), current_user: int =
              Depends(oauth2.get_curren_user), Limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # post =  db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=true).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def createpost(post: PostCreate, db: Session = Depends(get_db), current_user: int =
               Depends(oauth2.get_curren_user)):

    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/latest", response_model=PostResponse)
def get_latest_post(db: Session = Depends(get_db), current_user: int =
                    Depends(oauth2.get_curren_user)):
  
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()

    return post


@router.get("/{id}", response_model=Postout)
def get_post(id: int, db: Session = Depends(get_db), current_user: int =
             Depends(oauth2.get_curren_user)):
   
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post =  post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=true).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:

        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post was not found')

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id, db: Session = Depends(get_db), current_user: int =
                Depends(oauth2.get_curren_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} does not exist')

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perfrom requested action")
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int =
                Depends(oauth2.get_curren_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_id = post_query.first()

    if post_id == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} does not exist')
    if post_id.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perfrom requested action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
