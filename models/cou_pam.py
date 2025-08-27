from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db


class Cou_Pam(db.Model):
    __tablename__ = "cou_pam"
    id = Column(Integer, primary_key=True)
    pamphlet_id = Column(Integer, ForeignKey('pamphlets.id'), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False, index=True)

    pamphlet = db.relationship("Pamphlet", foreign_keys=[pamphlet_id], backref=backref("link_courses" , lazy="dynamic"))
    course = db.relationship("Course", foreign_keys=[course_id], backref=backref("link_pamphlets" , lazy="dynamic"))