from tokenize import String
from config import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy import ForeignKey, Integer, String 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Post(db.Model):
    ''' Post Data Model'''
    __tablename__ = 'post'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    repost_from_id = db.Column(Integer, ForeignKey('post.id'))
    quote_from_id = db.Column(Integer, ForeignKey('post.id'))
    user_id = db.Column(Integer, ForeignKey('user.id'))
    user = relationship("User")
    datetime_creation = db.Column(TIMESTAMP, server_default=func.now())
    text = db.Column(String(777))    
    repost_from = None
    quote_from = None

    def as_dict(self):
        obj = {c.name: getattr(self, c.name) for c in self.__table__.columns}        
        obj['user'] = {c.name: getattr(self.user, c.name) for c in self.user.__table__.columns}
        obj['repost_from'] = {}
        if self.repost_from_id:
            obj['repost_from'] = Post.query.get(self.repost_from_id).as_dict()
        obj['quote_from'] = {}
        if self.quote_from_id:
            obj['quote_from'] = Post.query.get(self.quote_from_id).as_dict()
        return obj