from datetime import datetime, timedelta
import pytz
from jose import jwt
from passlib.context import CryptContext
import logging
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from core import settings
from core.model import get_db, User
import ssl
from email.message import EmailMessage
import smtplib

logging.basicConfig(filename='../fundoo_notes.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def get_hash_password(plain_password):
        return pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password, hash_password):
        return pwd_context.verify(plain_password, hash_password)


class JWT:
    @staticmethod
    def jwt_encode(payload: dict):
        if 'exp' not in payload:
            payload.update(exp=datetime.now(pytz.utc) + timedelta(hours=1), iat=datetime.now(pytz.utc))
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def jwt_decode(token):
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except jwt.JWTError as e:
            raise e


def jwt_authorization(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get('authorization')
    decode_token = JWT.jwt_decode(token)
    user_id = decode_token.get('user_id')
    user = db.query(User).filter_by(id=user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized User')
    request.state.user = user


def send_verification_email(verification_token: str, email):
    email_sender = settings.email_sender
    email_password = settings.email_password

    subject = 'Email Verification'
    body = f"Click the link to verify your email: http://127.0.0.1:8000/user/verify?token={verification_token}"

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email, em.as_string())
        smtp.quit()

