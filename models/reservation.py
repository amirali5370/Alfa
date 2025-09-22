from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db


class Reservation(db.Model):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    camp_id = Column(Integer, ForeignKey('camps.id'), nullable=True, index=True)

    user = db.relationship("User", foreign_keys=[user_id], backref=backref("reservations" , lazy="dynamic"))
    camp = db.relationship("Camp", foreign_keys=[camp_id], backref=backref("reservations" , lazy="dynamic"))