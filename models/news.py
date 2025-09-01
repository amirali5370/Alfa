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
    is_event = Column(Integer, nullable=False, index=True)
    jalali_date = Column(String, nullable=False)