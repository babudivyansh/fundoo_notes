from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Column, String, BigInteger, create_engine, Boolean

engine = create_engine("postgresql+psycopg2://postgres:12345@localhost:5432/fundoo_notes")
session = Session(engine)
Base = declarative_base()


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, index=True)
    user_name = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    email = Column(String(50), unique=True)
    phone = Column(BigInteger)
    location = Column(String(100))
    password = Column(String(50))
    is_verified = Column(Boolean, default=False)

    def __repr__(self):
        return self.user_name
