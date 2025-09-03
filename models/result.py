from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db


class Result(db.Model):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True)
    score = Column(Integer, nullable=False, default=0)
    enter = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    quiz_id = Column(Integer, ForeignKey('quizes.id'), nullable=False, index=True)

    user = db.relationship("User", foreign_keys=[user_id], backref=backref("results" , lazy="dynamic"))
    quiz = db.relationship("Quiz", foreign_keys=[quiz_id], backref=backref("results" , lazy="dynamic"))