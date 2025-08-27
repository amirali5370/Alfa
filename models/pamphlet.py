from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db


class Pamphlet(db.Model):
    __tablename__ = "pamphlets"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True, index=True)
    auth = Column(String, nullable=False, index=True)
    grade_bits = Column(Integer, nullable=False, index=True)