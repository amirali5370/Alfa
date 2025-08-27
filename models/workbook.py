from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db


class Workbook(db.Model):
    __tablename__ = "workbooks"
    id = Column(Integer, primary_key=True)
    auth = Column(String, nullable=False, index=True)
    is_degree = Column(Integer, nullable=False, default=0, index=True)
    status = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    quiz_id = Column(Integer, ForeignKey('quizes.id'), nullable=True, index=True)

    user = db.relationship("User", foreign_keys=[user_id], backref=backref("workbooks" , lazy="dynamic"))
    quiz = db.relationship("Quiz", foreign_keys=[quiz_id], backref=backref("workbooks" , lazy="dynamic"))