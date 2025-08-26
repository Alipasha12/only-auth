from pydantic import BaseModel,Field,EmailStr

class UserCreate(BaseModel):
    full_name: str = Field(max_length=100,min_length=4)
    user_name: str = Field(max_length=100,min_length=4)
    password: str = Field(max_length=15,min_length=8)
    email: EmailStr
    phone_no: str = Field(max_length=13,min_length=8)
    gender: str
    
class Userlogin(BaseModel):
    email_or_username: str = Field(...,description="email_or_username")
    password: str = Field(...,min_length=6, max_length=18)