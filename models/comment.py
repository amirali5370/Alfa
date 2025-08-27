from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db


class Comment(db.Model):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    date = Column(Integer, nullable=False, index=True)
    status = Column(String, nullable=False, index=True)
    news_id = Column(Integer, ForeignKey('news.id'), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)

    news = db.relationship("News", foreign_keys=[news_id], backref=backref("comments" , lazy="dynamic"))
    user = db.relationship("User", foreign_keys=[user_id], backref=backref("comments" , lazy="dynamic"))