from db.schemas.base import Base
from sqlalchemy import Column, Integer, String, BLOB
from db.connect import get_db

class Violation(Base):
    __tablename__="violations"
    id = Column(Integer, primary_key=True)
    rider_img = Column(BLOB)
    plate_img = Column(BLOB)
    plate_txt = Column(String)


def add_violation(rider_img, plate_img, plate_txt=""):
    s = next(get_db())
    with s:
        try:
            violation = Violation(
                rider_img=rider_img,
                plate_img=plate_img,
                plate_txt=plate_txt
            )
            s.add(violation)
            s.commit()
        except Exception as e:
            print(e)
            s.rollback()

def get_violations():
    s = next(get_db())
    with s:
        try:
            violations = s.query(Violation).all()
            return violations
        except Exception as e:
            print(e)
        
def del_violation(violation_id):
    s = next(get_db())
    with s:
        try:
            violations = s.query(Violation).filter(Violation.id == violation_id).delete()
            s.commit()
        except Exception as e:
            print(e)
