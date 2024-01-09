"""
@Author: Divyansh Babu

@Date: 2024-01-04 12:40

@Last Modified by: Divyansh Babu

@Last Modified time: 2024-01-04 12:40

@Title : Fundoo Notes crud APIs.
"""
from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from core.model import get_db, Notes
from fastapi.responses import Response
from core.schema import NotesSchema, UpdateNote

router_notes = APIRouter()


@router_notes.post('/create', status_code=status.HTTP_201_CREATED, tags=["Notes"])
def create_note(payload: NotesSchema, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create fastapi for creating new note.
    Parameter: payload as NoteSchema object, response as Response object, db as database session.
    Return: Message of note added with status code 201.
    """
    try:
        body = payload.model_dump()
        notes = Notes(**body)
        db.add(notes)
        db.commit()
        db.refresh(notes)
        return {'message': 'Note Added', 'status': 201, 'data': body}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@router_notes.get('/get', status_code=status.HTTP_200_OK, tags=["Notes"])
def getting_all_note(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create api for getting data of all notes.
    Parameter: user as Userlogin object,response as Response object,db as database session.
    Return: Message of retrieved data with status code 200.
    """
    try:
        print(request.state.user)
        existing_note = db.query(Notes).filter_by(user_id=request.state.user.id).first()
        if existing_note:
            existing_note = db.query(Notes).all()
            return {'message': 'Data retrieved', 'status': 200, 'data': existing_note}
        return {'message': 'Invalid user id', 'status': 400}
    except Exception as e:
        response.status_code = 400
        return {'message': str(e), 'status': 400}


@router_notes.put('/update', status_code=status.HTTP_200_OK, tags=["Notes"])
def update_note(request: Request, payload: UpdateNote, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create api for updating the existing note.
    Parameter: note_id as int value, payload as NoteSchema object, title as query string,response as Response object,
    db as database session.
    Return: Message of contact added with status code 200.
    """
    try:
        note = db.query(Notes).filter_by(id=request.state.user.id).one_or_none()
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


@router_notes.delete("/delete", status_code=status.HTTP_200_OK, tags=["Notes"])
def delete_note(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create fastapi for deleting the contact into database.
    Parameter: title as query string,response as Response object,db as database session.
    Return: Message of contact added with status code 200.
    """
    try:
        existing_note = db.query(Notes).filter_by(id=request.state.user.id).one_or_none()
        if existing_note:
            db.delete(existing_note)
            db.commit()
            return {'message': 'Note Deleted', 'status': 200}
        raise HTTPException(detail='Note not found', status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response.status_code = 400
        return {'message': str(e), 'status': 400}
