from sqlalchemy import *
from extentions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    father_name = Column(String, nullable=True)
    code = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    school_name = Column(String, nullable=True)
    grade = Column(Integer, nullable=True, index=True)
    grade_name = Column(String, nullable=True, index=True)
    number = Column(String, nullable=True)
    addres = Column(String, nullable=True)
    birthday = Column(String, nullable=True)
    user_type = Column(String, nullable=True, default="student")
    coins = Column(Integer, nullable=True, index=True, default=0)
    pay = Column(Integer, nullable=True, default=0)
    completion = Column(Integer, nullable=True, default=0)
    invite_code = Column(String, nullable=True, unique=True)
    sub_invite_code = Column(String, nullable=True, unique=True)
    period_code = Column(Integer, nullable=True, index=True)