from sqlalchemy import *
from extentions import db


class Camp(db.Model):
    __tablename__ = "camps"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False, default=0)
    grade_bits = Column(Integer, nullable=False)
    auth = Column(String, nullable=False, index=True)
    status = Column(Integer, nullable=False, default=0)