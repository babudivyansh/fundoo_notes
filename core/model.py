"""
@Author: Divyansh Babu

@Date: 2024-01-04 12:40

@Last Modified by: Divyansh Babu

@Last Modified time: 2024-01-16 12:50

@Title : Fundoo Notes model module.
"""
from sqlalchemy.orm import declarative_base, Session, relationship
from sqlalchemy import Column, String, BigInteger, create_engine, Boolean, DateTime, ForeignKey, Table
from core.settings import DATABASE_NAME, DATABASE_PASSWORD

engine = create_engine(f"postgresql+psycopg2://postgres:{DATABASE_PASSWORD}@localhost:5432/{DATABASE_NAME}")
session = Session(engine)
Base = declarative_base()


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


collaborator = Table('collaborator', Base.metadata,
                     Column('user_id', BigInteger, ForeignKey('user.id')),
                     Column('note_id', BigInteger, ForeignKey('notes.id')))


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    email = Column(String(50), default='divyansh.verma525@gmail.com')
    phone = Column(BigInteger, default=9005202790)
    location = Column(String(100), default='Noida')
    password = Column(String)
    is_verified = Column(Boolean, default=False)
    notes = relationship('Notes', back_populates='user')
    label = relationship('Label', back_populates='user')
    note_m2m = relationship('Notes', secondary=collaborator, overlaps='user')

    def __repr__(self):
        return self.user_name


class Notes(Base):
    __tablename__ = 'notes'

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(500))
    color = Column(String(100))
    reminder = Column(DateTime, default=None)
    user_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='notes')
    user_m2m = relationship('User', secondary=collaborator, overlaps='notes')

    def __repr__(self):
        return self.title


class Label(Base):
    __tablename__ = 'label'

    id = Column(BigInteger, primary_key=True, index=True)
    label_name = Column(String(100))
    user_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='label')

    def __repr__(self):
        return self.label_name


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    request_method = Column(String)
    request_path = Column(String)
    count = Column(BigInteger, default=1)
    # user = Column(String, nullable=True)  # which user
