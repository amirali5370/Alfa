from sqlalchemy import *
from extentions import db


class News(db.Model):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    content = Column(String, nullable=False)
    prima_link = Column(String, nullable=False, index=True)
    auth = Column(String, nullable=False, index=True)
    grade_bits = Column(Integer, nullable=False, default=0, index=True)
    jalali_date = Column(String, nullable=False)
    xml_date = Column(String, nullable=False)