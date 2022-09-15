from tokenize import String
from config import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy import ForeignKey, Integer, String 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.Post import Post

Base = declarative_base()

class User(db.Model):
    ''' User Data model'''
    # table name
    __tablename__ = 'user'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(14), nullable=False)
    date_joined = db.Column(db.DateTime(timezone=True), server_default=func.now())
    total_posts = None

    def as_dict(self):
        obj = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        obj['date_joined'] = obj['date_joined'].strftime("%B %d, %Y")
        obj['total_posts'] = Post.query.filter(Post.user_id == self.id).count()

        return obj