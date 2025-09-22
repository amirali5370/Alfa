from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class Payment(db.Model):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    token = Column(String, nullable=False, index=True)
    status = Column(String, index=True)
    error = Column(String, index=True)
    refid = Column(String, index=True)
    transaction_id = Column(String, index=True)
    amount = Column(String, index=True)
    card_pan = Column(String, index=True)
    date = Column(String, index=True)

    inApp = Column(Integer, index=True, default=0)

    user = db.relationship("User", backref=backref("payments" , lazy="dynamic"))