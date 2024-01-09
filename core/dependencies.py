from datetime import timedelta, datetime
from typing import Union
from jose import jwt
from sqlalchemy.orm import Session
from core.model import User
from core import settings
from core.utils import Hasher
import pytz


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter_by(username=username).first()
    if (not user) or (not Hasher.verify_password(password, user.password)):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(pytz.utc) + expires_delta
    else:
        expire = datetime.now(pytz.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
