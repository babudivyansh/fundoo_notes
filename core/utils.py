"""
@Author: Divyansh Babu

@Date: 2024-01-16 12:40

@Last Modified by: Divyansh Babu

@Last Modified time: 2024-01-16 11:04

@Title : Fundoo Notes utils module.
"""
from datetime import datetime, timedelta
import pytz
from jose import jwt
from passlib.context import CryptContext
import logging
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from core import settings
from core.model import get_db, User, RequestLog
import ssl
from email.message import EmailMessage
import smtplib
import redis
from core.settings import PORT, HOST

logging.basicConfig(filename='./fundoo_notes.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

redis_obj = redis.Redis(host=HOST, port=PORT, decode_responses=True)


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
            logger.exception(e)


def jwt_authorization(request: Request, db: Session = Depends(get_db)):
    """
    Description: This function decode jwt token.
    Parameter: response as Response object, db as database session.
    Return: None
    """
    token = request.headers.get('authorization')
    decode_token = JWT.jwt_decode(token)
    user_id = decode_token.get('user_id')
    user = db.query(User).filter_by(id=user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized User')
    request.state.user = user


def send_verification_email(verification_token: str, email):
    """
    Description: This function send mail to verify user.
    Parameter: verification_token as string, email of user where send the mailto verify.
    Return: None
    """
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


class Redis:
    @staticmethod
    def add_redis(name, key, value):
        """
        Description: This function add and update data in redis memory.
        Parameter: name, key, value as parameter.
        Return: set the name, key, value to redis memory
        """
        return redis_obj.hset(name, key, value)

    @staticmethod
    def get_redis(name):
        """
        Description: This function get all data from redis memory.
        Parameter: name as parameter.
        Return: get all data from the redis memory using name.
        """
        return redis_obj.hgetall(name)

    @staticmethod
    def delete_redis(name, key):
        """
        Description: This function delete data from redis memory.
        Parameter: name, key as parameter.
        Return: delete data from redis using name and list of key.
        """
        return redis_obj.hdel(name, key)


def request_loger(request):
    """
    Description: This function update the middleware table in database.
    Parameter: response as parameter.
    Return: None
    """
    session = get_db()
    db = next(session)
    log = db.query(RequestLog).filter_by(request_method=request.method,
                                         request_path=request.url.path).one_or_none()
    if not log:
        log = RequestLog(request_method=request.method, request_path=request.url.path, count=1)
        db.add(log)
    else:
        log.count += 1

    db.commit()
