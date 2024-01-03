"""
@Author: Divyansh Babu

@Date: 2024-01-02 19:44

@Last Modified by: Divyansh Babu

@Last Modified time: 2024-01-02 19:44

@Title : Fundoo Notes using FastAPI.
"""
from fastapi import FastAPI
from routes.user import router
app = FastAPI()

app.include_router(router, prefix='/user')

