import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import streamlit as st
from sqlalchemy.exc import IntegrityError


@st.cache_resource
def get_engine():
    print()
    engine = create_engine('sqlite:///src/db/helmet_lp_db.sqlite3')
    return engine

sessionLocal = sessionmaker(bind=get_engine())

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()



