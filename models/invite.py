from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db


class Invite(db.Model):
    __tablename__ = "invites"
    id = Column(Integer, primary_key=True)
    assistant = Column(Integer, nullable=False, default=0, index=True)
    activate = Column(Integer, nullable=False, default=0)
    inviter_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    invitee_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)

    inviter = db.relationship("User", foreign_keys=[inviter_id], backref=backref("sent_invitations" , lazy="dynamic"))
    invitee = db.relationship("User", foreign_keys=[invitee_id], backref=backref("received_invitations" , lazy="dynamic"))