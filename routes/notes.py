"""
@Author: Divyansh Babu

@Date: 2024-01-04 12:40

@Last Modified by: Divyansh Babu

@Last Modified time: 2024-01-04 12:40

@Title : Fundoo Notes crud APIs.
"""
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from model import User, get_db, Notes
from fastapi.responses import Response
from routes.user import Userlogin
from schema import NotesSchema
from pwd_hashing import Hasher

router_notes = APIRouter()


@router_notes.post('/create/', status_code=status.HTTP_201_CREATED)
def create_note(payload: NotesSchema, user: Userlogin, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create fastapi for creating new note.
    Parameter: payload as NoteSchema object,user as UserLogin object, response as Response object,
    db as database session.
    Return: Message of note added with status code 201.
    """
    try:
        data = db.query(User).filter_by(user_name=user.user_name).one_or_none()
        if not data:
            raise HTTPException(detail='Username Not valid', status_code=status.HTTP_401_UNAUTHORIZED)
        if not Hasher.verify_password(user.password, data.password):
            raise HTTPException(detail='Password Not valid', status_code=status.HTTP_401_UNAUTHORIZED)

        body = payload.model_dump()
        body['user_id'] = data.id
        notes = Notes(**body)
        db.add(notes)
        db.commit()
        db.refresh(notes)
        return {'message': 'Note Added', 'status': 201, 'data': body}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@router_notes.get('/get/', status_code=status.HTTP_200_OK)
def getting_all_note(user: Userlogin, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create api for getting data of all notes.
    Parameter: user as Userlogin object,response as Response object,db as database session.
    Return: Message of retrieved data with status code 200.
    """
    try:
        data = db.query(User).filter_by(user_name=user.user_name).one_or_none()
        if not data:
            raise HTTPException(detail='Username Not valid', status_code=status.HTTP_401_UNAUTHORIZED)
        if not Hasher.verify_password(user.password, data.password):
            raise HTTPException(detail='Password Not valid', status_code=status.HTTP_401_UNAUTHORIZED)
        if data is not None:
            existing_note = db.query(Notes).filter_by(user_id=data.id).all()
        else:
            existing_note = db.query(Notes).all()
        return {'message': 'Data retrieved', 'status': 200, 'data': existing_note}
    except Exception as e:
        response.status_code = 400
        return {'message': str(e), 'status': 400}


@router_notes.put('/update/{note_id}', status_code=status.HTTP_200_OK)
def update_note(note_id: int, payload: NotesSchema, user: Userlogin, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create api for updating the existing note.
    Parameter: note_id as int value, payload as NoteSchema object, user as Userlogin object,response as Response object,
    db as database session.
    Return: Message of contact added with status code 200.
    """
    try:
        user_data = db.query(User).filter_by(user_name=user.user_name).one_or_none()
        if not user_data:
            raise HTTPException(detail='Username Not valid', status_code=status.HTTP_401_UNAUTHORIZED)
        if not Hasher.verify_password(user.password, user_data.password):
            raise HTTPException(detail='Password Not valid', status_code=status.HTTP_401_UNAUTHORIZED)

        note = db.query(Notes).filter_by(id=note_id, user_id=user_data.id).first()
        if not note:
            raise HTTPException(detail='Note not found', status_code=status.HTTP_404_NOT_FOUND)

        updated_data = payload.model_dump()
        for key, value in updated_data.items():
            setattr(note, key, value)

        db.commit()
        db.refresh(note)
        return {'message': 'Note updated', 'status': 200, 'data': updated_data}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(e), 'status': 400}


@router_notes.delete("/delete/", status_code=status.HTTP_200_OK)
def delete_note(user: Userlogin, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create fastapi for deleting the contact into database.
    Parameter: user as Userlogin object,response as Response object,db as database session.
    Return: Message of contact added with status code 200.
    """
    try:
        data = db.query(User).filter_by(user_name=user.user_name).one_or_none()
        if not data:
            raise HTTPException(detail='Username Not valid', status_code=status.HTTP_401_UNAUTHORIZED)
        if not Hasher.verify_password(user.password, data.password):
            raise HTTPException(detail='Password Not valid', status_code=status.HTTP_401_UNAUTHORIZED)
        existing_note = db.query(Notes).filter_by(user_id=data.id).first()
        db.delete(existing_note)
        db.commit()

        return {'message': 'Note Deleted', 'status': 200}
    except Exception as e:
        response.status_code = 400
        return {'message': str(e), 'status': 400}
