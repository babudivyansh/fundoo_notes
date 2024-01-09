"""
@Author: Divyansh Babu

@Date: 2024-01-02 19:44

@Last Modified by: Divyansh Babu

@Last Modified time: 2024-01-02 19:44

@Title : Fundoo Notes using FastAPI.
"""
from fastapi import FastAPI, Security, Depends
from fastapi.security import APIKeyHeader
from routes.user import router_user
from routes.notes import router_notes
from core.utils import jwt_authorization
app = FastAPI()

app.include_router(router_user, prefix='/user')

app.include_router(router_notes, prefix='/note', dependencies=[Security(APIKeyHeader(name="authorization")), Depends(jwt_authorization)])
