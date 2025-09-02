from sqlalchemy import *
from extentions import db


class Course(db.Model):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Integer, nullable=False)
    content_link = Column(Integer, nullable=False, index=True)
    prima_link = Column(String, nullable=False, unique=True, index=True)
    grade_bits = Column(Integer, nullable=False)
