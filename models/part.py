from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db


class Part(db.Model):
    __tablename__ = "parts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    auth = Column(String, nullable=False, index=True)
    content_link = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

    course = db.relationship("Course", foreign_keys=[course_id], backref=backref("parts" , lazy="dynamic"))