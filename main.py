"""
@Author: Divyansh Babu

@Date: 2024-01-02 19:44

@Last Modified by: Divyansh Babu

@Last Modified time: 2024-01-02 19:44

@Title : Fundoo Notes using FastAPI.
"""
from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session
from model import User, get_db
from schema import UserDetails, Userlogin
from fastapi.responses import Response

app = FastAPI()


@app.post("/post/", status_code=status.HTTP_201_CREATED)
def user_registration(body: UserDetails, response: Response, db: Session = Depends(get_db)):
    try:
        body = body.model_dump()
        existing_user = User(**body)
        db.add(existing_user)
        db.commit()
        db.refresh(existing_user)
        return {'message': 'user Added', 'status': 201, 'data': existing_user}
    except Exception as e:
        response.status_code = 400
        return {"message": str(e), "status": 400}


@app.post("/login/", status_code=status.HTTP_200_OK)
def user_login(payload: Userlogin, response: Response, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.user_name == payload.user_name and User.password == payload.password).first()
        if not user:
            raise HTTPException(status_code=404, detail="Invalid Credential")
        return {'message': 'Login successful', 'status': 200, 'data': payload.model_dump()}
    except Exception as e:
        response.status_code = 400
        return {'message': str(e), 'status': 400}
