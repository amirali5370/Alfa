from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db


class Cou_Qui(db.Model):
    __tablename__ = "cou_qui"
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quizes.id'), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False, index=True)

    quiz = db.relationship("Quiz", foreign_keys=[quiz_id], backref=backref("link_courses" , lazy="dynamic"))
    course = db.relationship("Course", foreign_keys=[course_id], backref=backref("link_quizes" , lazy="dynamic"))