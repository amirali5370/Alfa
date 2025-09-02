from sqlalchemy import *
from extentions import db


class Quiz(db.Model):
    __tablename__ = "quizes"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    auth = Column(String, nullable=False, index=True)
    count = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    status = Column(String, nullable=False)
    grade_bits = Column(Integer, nullable=False)
    start_jalali = Column(String, nullable=False)
    end_jalali = Column(String, nullable=False)
