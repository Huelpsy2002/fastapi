from os import stat
from fastapi import APIRouter , Depends , status , HTTPException , Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import schemas
from .. import database, oauth2 , models ,utils

router = APIRouter(tags=['Authentaction'])

@router.post('/login' , response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends() , db:Session = Depends(database.get_db)):
    

     user =  db.query(models.User).filter(models.User.email ==user_credentials.username).first()
     if not user:

       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"invalid credentials")
 
     if not utils.verify(user_credentials.password , user.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,detail=f"invalid credentials")

     access_token = oauth2.create_acsses_token(data = {"user_id":user.id})
     return {"access_token":access_token , "token_type":"bearer"}