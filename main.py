"""
@Author: Divyansh Babu

@Date: 2024-01-02 19:44

@Last Modified by: Divyansh Babu

@Last Modified time: 2024-01-23 19:22

@Title : Fundoo Notes using FastAPI.
"""
from fastapi import FastAPI, Security, Depends, Request
from fastapi.security import APIKeyHeader
from routes.user import router_user
from routes.notes import router_notes
from routes.label import router_label
from core.utils import jwt_authorization, request_loger
import warnings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

warnings.filterwarnings("ignore")


@app.middleware("http")
async def addmiddleware(request: Request, call_next):
    response = await call_next(request)
    request_loger(request)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add the origin of frontend application
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_user, prefix='/user')

app.include_router(router_notes, prefix='/note',
                   dependencies=[Security(APIKeyHeader(name="authorization")), Depends(jwt_authorization)])

app.include_router(router_label, prefix='/label',
                   dependencies=[Security(APIKeyHeader(name="authorization")), Depends(jwt_authorization)])
