from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    username: str
    email:str
    password:str =Field(min_length= 6)

class ProductCreate(BaseModel):
    name:str
    price:int = Field(gt=0)


#=============Login =============
class UserLogin(BaseModel):
    username: str
    password: str