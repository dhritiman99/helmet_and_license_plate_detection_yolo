from db.connect import get_engine
from db.schemas.base import Base
from db.schemas.user import User
from db.schemas.violation import Violation


def init_db():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)