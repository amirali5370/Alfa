from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db


class Question(db.Model):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    option_1 = Column(String, nullable=False)
    option_2 = Column(String, nullable=False)
    option_3 = Column(String, nullable=True)
    option_4 = Column(String, nullable=True)
    option_5 = Column(String, nullable=True)
    answer = Column(Integer, nullable=False)
    quiz_id = Column(Integer, ForeignKey('quizes.id'), nullable=False)

    quiz = db.relationship("Quiz", foreign_keys=[quiz_id], backref=backref("questions" , lazy="dynamic"))