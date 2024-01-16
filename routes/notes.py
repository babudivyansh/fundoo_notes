"""
@Author: Divyansh Babu

@Date: 2024-01-04 12:40

@Last Modified by: Divyansh Babu

@Last Modified time: 2024-01-16 10:48

@Title : Fundoo Notes crud APIs.
"""
import json
from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from core.model import get_db, Notes, User, collaborator
from fastapi.responses import Response
from core.schema import NotesSchema, CollaboratorSchema
from core.utils import logger, Redis

router_notes = APIRouter()


@router_notes.post('/create', status_code=status.HTTP_201_CREATED, tags=["Notes"])
def create_note(payload: NotesSchema, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create fastapi for creating new note.
    Parameter: payload as NoteSchema object, response as Response object, db as database session.
    Return: Message of note added with status code 201.
    """
    try:
        body = payload.model_dump()
        body.update({'user_id': request.state.user.id})
        notes = Notes(**body)
        db.add(notes)
        db.commit()
        db.refresh(notes)
        Redis.add_redis(f"user_{notes.user_id}", f"notes_{notes.id}", json.dumps(body))
        return {'message': 'Note Added', 'status': 201, 'data': body}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception(e)
        return {"message": str(e)}


@router_notes.get('/get', status_code=status.HTTP_200_OK, tags=["Notes"])
def getting_all_note(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create api for getting data of all notes.
    Parameter: user as Userlogin object,response as Response object,db as database session.
    Return: Message of retrieved data with status code 200.
    """
    try:
        redis_cons = Redis.get_redis(f"user_{request.state.user.id}")
        if redis_cons:
            # Convert the string representation to a dictionary
            for key, value in redis_cons.items():
                redis_cons[key] = json.loads(value)
            return {'message': 'Data retrieved', 'status': 200, 'data': redis_cons}
        existing_note = db.query(Notes).filter_by(user_id=request.state.user.id).all()
        collab_notes = db.query(collaborator).filter_by(user_id=request.state.user.id).all()
        notes = db.query(Notes).filter(Notes.id.in_(list(map(lambda x: x.note_id, collab_notes)))).all()
        existing_note.extend(notes)
        return {'message': 'Data retrieved', 'status': 200, 'data': existing_note}
    except Exception as e:
        response.status_code = 400
        logger.exception(e)
        return {'message': str(e), 'status': 400}


@router_notes.put('/update/{note_id}', status_code=status.HTTP_200_OK, tags=["Notes"])
def update_note(note_id: int, request: Request, payload: NotesSchema, response: Response,
                db: Session = Depends(get_db)):
    """
    Description: This function create api for updating the existing note.
    Parameter: note_id as int value, payload as NoteSchema object, title as query string,response as Response object,
    db as database session.
    Return: Message of contact added with status code 200.
    """
    try:
        note = db.query(Notes).filter_by(user_id=request.state.user.id, id=note_id).one_or_none()
        if not note:
            raise HTTPException(detail='Note not found', status_code=status.HTTP_404_NOT_FOUND)

        updated_data = payload.model_dump()
        [setattr(note, key, value) for key, value in updated_data.items()]
        db.commit()
        db.refresh(note)
        Redis.add_redis(f"user_{request.state.user.id}", f"notes_{note.id}", json.dumps(updated_data))

        return {'message': 'Note updated', 'status': 200, 'data': updated_data}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception(e)
        return {'message': str(e), 'status': 400}


@router_notes.delete("/delete/{id}", status_code=status.HTTP_200_OK, tags=["Notes"])
def delete_note(note_id: int, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create fastapi for deleting the contact into database.
    Parameter: title as query string,response as Response object,db as database session.
    Return: Message of contact added with status code 200.
    """
    try:
        existing_note = db.query(Notes).filter_by(user_id=request.state.user.id, id=note_id).one_or_none()
        if existing_note:
            db.delete(existing_note)
            db.commit()
            Redis.delete_redis(f"user_{request.state.user.id}", *f"notes_{note_id}")
            return {'message': 'Note Deleted', 'status': 200}
        raise HTTPException(detail='Note not found', status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response.status_code = 400
        logger.exception(e)
        return {'message': str(e), 'status': 400}


@router_notes.post('/add_collaborator', status_code=status.HTTP_201_CREATED, tags=["Notes"])
def add_collaborator(payload: CollaboratorSchema, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: Add a collaborator to a specific note.
    Parameter: payload as CollaboratorSchema object containing note_id and user_id,
               request as Request object, response as Response object, db as database session.
    Return: Message indicating the collaborator addition with status code 200.
    """
    try:
        note = db.query(Notes).filter_by(user_id=request.state.user.id, id=payload.note_id).first()
        if not note:
            raise HTTPException(detail='Note not found', status_code=status.HTTP_404_NOT_FOUND)

        for collaborator_id in payload.user_id:
            if collaborator_id != request.state.user.id:
                body = db.query(User).filter_by(id=collaborator_id).first()
                if body:
                    # Check if the collaborator is already added to the note
                    if body not in note.user_m2m:
                        note.user_m2m.append(body)
                else:
                    raise HTTPException(detail=f'User with id {collaborator_id} not found',
                                        status_code=status.HTTP_404_NOT_FOUND)

        db.commit()
        return {'message': 'Collaborators added to the note', 'status': 201}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception(e)
        return {'message': str(e), 'status': 400}


@router_notes.delete('/remove_collaborator', status_code=status.HTTP_200_OK, tags=["Notes"])
def remove_collaborator(payload: CollaboratorSchema, request: Request, response: Response,
                        db: Session = Depends(get_db)):
    """
    Description: Remove a collaborator from a specific note.
    Parameter: payload as CollaboratorSchema object containing note_id and user_id,
               request as Request object, response as Response object, db as database session.
    Return: Message indicating the collaborator removal with status code 200.
    """
    try:
        note = db.query(Notes).filter_by(user_id=request.state.user.id, id=payload.note_id).first()
        if not note:
            raise HTTPException(detail='Note not found', status_code=status.HTTP_404_NOT_FOUND)

        for collaborator_id in payload.user_id:
            if collaborator_id != request.state.user.id:
                body = db.query(User).filter_by(id=collaborator_id).first()
                if body:
                    # Check if the collaborator is in the note's collaborators list and remove if present
                    if body in note.user_m2m:
                        note.user_m2m.remove(body)
                else:
                    raise HTTPException(detail=f'User with id {collaborator_id} not found',
                                        status_code=status.HTTP_404_NOT_FOUND)

        db.commit()
        return {'message': 'Collaborators removed from the note', 'status': 200}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception(e)
        return {'message': str(e), 'status': 400}
