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


class UpdateNote(BaseModel):
    title: str
    description: str
    color: str


class NotesSchema(UpdateNote):
    user_id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(BaseModel):
    access_token: Token
    refresh_token: Token


class TokenData(BaseModel):
    user_id: int | None = None

    class Config:
        arbitrary_types_allowed = True
