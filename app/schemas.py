
from operator import le
from typing import Optional
from pydantic import BaseModel, conint
from datetime import datetime
from pydantic import EmailStr
   
class PostBase(BaseModel):
    
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    id:int
    email: EmailStr
    created_at:datetime

    class Config:
        orm_mode = True



class PostResponse(PostBase):
    id:int
    user_id:int
   
    created_at:datetime
    user:UserResponse
 
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str        
class UserResponse(BaseModel):
    id:int
    email: EmailStr
    created_at:datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str]   = None  



class Vote(BaseModel):
    post_id:int 
    dir: conint(le = 1 , ge=0)  


class Postout(BaseModel):
    Post:PostResponse
    votes:int
    class Config:
        orm_mode = True
