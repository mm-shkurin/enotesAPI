from pydantic import *

class UserBase(BaseModel):
    vk_id : int
    email : EmailStr
    first_name : str
    last_name : str

class UserCreate(UserBase):
    access_token : str

class UserResponse(UserBase):
    id:int

    class Config : 
        from_attributes = True

class Token(BaseModel):
    access_token : str 
    token_type : str