from sqlalchemy import *
from extentions import db


class Ticket(db.Model):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False)
    message = Column(String, nullable=False)