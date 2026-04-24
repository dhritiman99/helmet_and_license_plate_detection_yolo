from sqlalchemy import Integer, Column, String
from db.schemas.base import Base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from db.connect import get_db

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

def login_user(username, password):
    if username == '' or password == '':
        return None
    s = next(get_db())
    with s:
        user = s.query(User).filter_by(
            name=username,
            password=password
        ).first()
        return user

def add_user(name, email, password):
    s = next(get_db())
    with s:
        try:
            new_user = User(
                name=name,
                password=password,
                email=email
            )
            s.add(new_user)
            s.commit()
        except Exception as e:
            s.rollback()
