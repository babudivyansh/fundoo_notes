from pydantic import BaseModel, Field, EmailStr


class UserDetails(BaseModel):
    user_name: str
    password: str
    email: EmailStr
    first_name: str = Field(pattern=r"^[A-Z]{1}\D{3,}$")
    last_name: str = Field(pattern=r"^[A-Z]{1}\D{3,}$")
    location: str
    phone: int


class Userlogin(BaseModel):
    user_name: str
    password: str
