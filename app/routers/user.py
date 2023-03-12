from app import models,utils
from fastapi import  status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import  Session
from .. schemas import  UserCreate, UserResponse
from .. database import get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags= ['Users']

)






#////////////////////////////////////////// USERS //////////////////////////////////////////////////////////////////////

@router.post("/", status_code=status.HTTP_201_CREATED , response_model=UserResponse )

def create_user(user:UserCreate,db: Session = Depends(get_db)):

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_User = models.User(**user.dict())
    db.add(new_User)
    db.commit()
    db.refresh(new_User)


    return new_User

@router.get("/",status_code=status.HTTP_200_OK , response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    user =  db.query(models.User).all()
    return  user


@router.get('/{id}' , response_model=UserResponse)
def get_user(id:int , db: Session = Depends(get_db)):
    user =  db.query(models.User).filter(models.User.id ==id).first()

    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"User with id:{id} not found")





    return user

