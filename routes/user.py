from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from core.model import User, get_db
from core.schema import UserDetails, Userlogin
from core.utils import Hasher, JWT, send_verification_email

router_user = APIRouter()
jwt_handler = JWT()


@router_user.post("/post/", status_code=status.HTTP_201_CREATED, tags=["User"])
def user_registration(body: UserDetails, response: Response, db: Session = Depends(get_db)):
    try:
        user_data = body.model_dump()
        user_data['password'] = Hasher.get_hash_password(user_data['password'])
        new_user = User(**user_data)
        db.add(new_user)
        db.commit()
        token = jwt_handler.jwt_encode({'user_id': new_user.id})
        send_verification_email(token, new_user.email)
        db.refresh(new_user)
        return {"status": 201, "message": "Registered"}
    except Exception as e:
        response.status_code = 400
        return {"message": e.args[0], 'status': 400, 'data': {}}


@router_user.post("/login/", status_code=status.HTTP_200_OK, tags=["User"])
def user_login(payload: Userlogin, response: Response, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter_by(user_name=payload.user_name).first()
        if user.is_verified is True:
            if user or Hasher.verify_password(payload.password, user.password):
                token = jwt_handler.jwt_encode({'user_id': user.id})
                return {'status': 200, "message": 'Logged in successfully', 'access_token': token}
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"message": 'Invalid username or password', 'status': 400, 'data': {}}
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": 'User is not verified', 'status': 400, 'data': {}}

    except Exception as e:
        response.status_code = 400
        return {"message": e.args[0], 'status': 400, 'data': {}}


@router_user.get("/verify")
def verify_user(token: str, db: Session = Depends(get_db)):
    decode_token = JWT.jwt_decode(token)
    user_id = decode_token.get('user_id')
    user = db.query(User).filter_by(id=user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized User')
    user.is_verified = True
    db.commit()
    return {'status': 200, "message": 'User verified successfully'}
