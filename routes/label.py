"""
@Author: Divyansh Babu

@Date: 2024-01-04 12:40

@Last Modified by: Divyansh Babu

@Last Modified time: 2024-01-16 10:45

@Title : Label crud APIs.
"""
from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from core.model import get_db, Label
from fastapi.responses import Response
from core.schema import LabelSchema
from core.utils import logger


router_label = APIRouter()


@router_label.post('/create', status_code=status.HTTP_201_CREATED, tags=["Label"])
def create_label(payload: LabelSchema, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function for creating new label.
    Parameter: payload as LabelSchema object, request as request object, response as Response object,
    db as database session.
    Return: Message of label added with status code 201.
    """
    try:
        body = payload.model_dump()
        body.update({'user_id': request.state.user.id})
        labels = Label(**body)
        db.add(labels)
        db.commit()
        db.refresh(labels)
        return {'message': 'Label Added', 'status': 201, 'data': body}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception(e)
        return {"message": str(e)}


@router_label.get('/get', status_code=status.HTTP_200_OK, tags=["Label"])
def getting_all_label(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create api for getting data of all labels.
    Parameter: user as Userlogin object,request as Request object, response as Response object,db as database session.
    Return: Message of retrieved data with status code 200.
    """
    try:
        existing_label = db.query(Label).filter_by(user_id=request.state.user.id).all()
        return {'message': 'Data retrieved', 'status': 200, 'data': existing_label}
    except Exception as e:
        response.status_code = 400
        logger.exception(e)
        return {'message': str(e), 'status': 400}


@router_label.put('/update/{label_id}', status_code=status.HTTP_200_OK, tags=["Label"])
def update_label(label_id: int, request: Request, payload: LabelSchema, response: Response,
                 db: Session = Depends(get_db)):
    """
    Description: This function create api for updating the existing note.
    Parameter: note_id as int value, payload as labelSchema object, request as Request object,
    response as Response object, db as database session.
    Return: Message of label added with status code 200.
    """
    try:
        label = db.query(Label).filter_by(user_id=request.state.user.id, id=label_id).one_or_none()
        if not label:
            raise HTTPException(detail='Label not found', status_code=status.HTTP_404_NOT_FOUND)

        updated_data = payload.model_dump()
        [setattr(label, key, value) for key, value in updated_data.items()]
        db.commit()
        db.refresh(label)
        return {'message': 'Label updated', 'status': 200, 'data': updated_data}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception(e)
        return {'message': str(e), 'status': 400}


@router_label.delete("/delete/{id}", status_code=status.HTTP_200_OK, tags=["Label"])
def delete_label(label_id: int, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create fastapi for deleting the label into database.
    Parameter: label_id as path parameter,request as Request object,response as Response object,db as database session.
    Return: Message of label deleted with status code 200.
    """
    try:
        existing_label = db.query(Label).filter_by(user_id=request.state.user.id, id=label_id).one_or_none()
        if existing_label:
            db.delete(existing_label)
            db.commit()
            return {'message': 'Label Deleted', 'status': 200}
        raise HTTPException(detail='Label not found', status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response.status_code = 400
        logger.exception(e)
        return {'message': str(e), 'status': 400}
