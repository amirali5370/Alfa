from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db
from config import SPECIAL_1_AMOUNT


class Special_1(db.Model):
    __tablename__ = "special_1"

    id = Column(Integer, primary_key=True)
    auth = Column(String, nullable=False, unique=True, index=True)
    code = Column(String, nullable=False, unique=True)
    relationship = Column(String, nullable=True)
    special_code = Column(String, nullable=False, unique=True)
    amount = Column(Integer, default=SPECIAL_1_AMOUNT)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = db.relationship("User", foreign_keys=[user_id], backref=backref("special_data" , lazy="dynamic"))