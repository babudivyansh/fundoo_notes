from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from main import app
from core.model import get_db, Base
from core.settings import DATABASE_PASSWORD

engine = create_engine(f'postgresql+psycopg2://postgres:{DATABASE_PASSWORD}@localhost:5432/test_fundoo_notes')
session = Session(engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# pytest mark.abc

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)


@pytest.fixture
def user_data():
    return {
        "user_name": "divyanshbabu03@gmail.com",
        "first_name": "Divyansh",
        "last_name": "Babu",
        "email": "omkarbhise8635@gmail.com",
        "password": "Divyansh123",
        "phone": 9005202790,
        "location": "Noida",
        "is_verified": True
    }


@pytest.fixture
def login_data():
    return {
        "user_name": "divyanshbabu03@gmail.com",
        "password": "Divyansh123"
    }


@pytest.fixture
def notes_data():
    return {
        "title": "Pytest",
        "description": "using TestClient test the apis",
        "color": "red"
    }


@pytest.fixture
def new_notes_data():
    return {
        "title": "Override the get_db",
        "description": "for the api testing we are override the get_db function with override_get_db function",
        "color": "red"
    }


@pytest.fixture
def update_notes_data():
    return {
        "title": "Pytest",
        "description": "using TestClient test the apis",
        "color": "pink"
    }


@pytest.fixture
def label_data():
    return {
        'label_name': "python "
    }


@pytest.fixture
def update_label_data():
    return {
        'label_name': "python FastAPI "
    }
