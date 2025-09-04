from sqlalchemy import *
from extentions import db


class Webinar(db.Model):
    __tablename__ = "webinars"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    teacher = Column(String, nullable=True)
    content_link = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    grade_bits = Column(Integer, nullable=False)
    start_jalali = Column(String, nullable=False)
    end_jalali = Column(String, nullable=False)
