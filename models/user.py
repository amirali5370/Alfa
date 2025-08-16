from sqlalchemy import *
# from sqlalchemy.orm import backref
from extentions import db

from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)