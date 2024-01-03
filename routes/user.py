from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from model import User, get_db
from schema import UserDetails, Userlogin
from fastapi.responses import Response
from pwd_hashing import Hasher

router = APIRouter()


@router.post("/post/", status_code=status.HTTP_201_CREATED)
def user_registration(body: UserDetails, response: Response, db: Session = Depends(get_db)):
    try:
        body = body.model_dump()
        body['password'] = Hasher.get_hash_password(body['password'])
        existing_user = User(**body)
        db.add(existing_user)
        db.commit()
        db.refresh(existing_user)
        return {'message': 'user Added', 'status': 201, 'data': existing_user}
    except Exception as e:
        response.status_code = 400
        return {"message": str(e), "status": 400}


@router.post("/login/", status_code=status.HTTP_200_OK)
def user_login(payload: Userlogin, response: Response, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter_by(user_name=payload.user_name).one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid Credential")
        if not Hasher.verify_password(payload.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid Credential")
        return {'message': 'Login successful', 'status': 200}
    except Exception as e:
        response.status_code = 400
        return {'message': str(e), 'status': 400}
