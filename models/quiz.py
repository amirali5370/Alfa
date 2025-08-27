from sqlalchemy import *
from extentions import db


class Quiz(db.Model):
    __tablename__ = "quizes"
    id = Column(Integer, primary_key=True)
    auth = Column(String, nullable=False, index=True)
    count = Column(Integer, nullable=False)
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    status = Column(String, nullable=False, index=True)
    grade_bits = Column(Integer, nullable=False)