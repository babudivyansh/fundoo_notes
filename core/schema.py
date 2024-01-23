"""
@Author: Divyansh Babu

@Date: 2024-01-06 19:44

@Last Modified by: Divyansh Babu

@Last Modified time: 2024-01-23 19:24

@Title : Fundoo Notes schema module.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import List


class UserDetails(BaseModel):
    user_name: str = Field(default='Enter user name', title='Enter User name')
    password: str = Field(default='Enter user password', title='Enter User password', min_length=8)
    email: EmailStr = Field(default='Enter email id', title='Enter your email')
    first_name: str = Field(default='Enter First Name', title='Enter First Name', pattern=r"^[A-Z]{1}\D{3,}$")
    last_name: str = Field(default='Enter Last Name', title='Enter Last Name', pattern=r"^[A-Z]{1}\D{3,}$")
    location: str = Field(default='Enter your City Name', title='Enter your City Name')
    phone: int = Field(default='Enter phone number', title='Enter phone number')


class Userlogin(BaseModel):
    user_name: str = Field(default='Enter user name', title='Enter User name')
    password: str = Field(default='Enter user password', title='Enter User password')


class NotesSchema(BaseModel):
    title: str = Field(default='Enter title', title='Enter title')
    description: str = Field(default='Enter description', title='Enter description')
    color: str = Field(default='Enter color', title='Enter color')


class LabelSchema(BaseModel):
    label_name: str = Field(default='Enter label name', title='Enter label name')


class CollaboratorSchema(BaseModel):
    note_id: int = Field(title='Enter note id')
    user_id: List[int]
