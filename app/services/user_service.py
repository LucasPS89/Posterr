#!/usr/bin/env python
from turtle import home
from models.models import User, Post
from config import db
from werkzeug.exceptions import NotFound
from sqlalchemy.orm import sessionmaker
from services.queries import queries


def get(user_id=None):
    '''
    Get all users or user by id
    :returns: User entity
    '''
    if user_id:
        user =  User.query.get(user_id)
        qty = get_total_posts(user_id)
        user.set_total_posts(qty)
        return user
    else:         
        return User.query.all()

def get_user_posts(user_id=None):
    homepage = queries.get_homepage(db.engine.raw_connection(), user_id=user_id, )
    posts=[]
    for p in homepage:
        post = {
            'user_id':  p[0],
            'post': p[1],
            'quote_from_id': p[2],
            'quote_from': p[3],
            'repost_from_id': p[4],
            'repost_from': p[5],
            'datetime_creation': p[6]
        }
        posts.append(post)
    return posts




def post(body):
    '''
    Create entity with body
    :param body: request body
    :returns: the created entity
    '''
    user = User(**body)
    
    if check_if_exists(user.username):
        raise Exception(f"The username {user.username} already exists")
    if len(user.username) > 14:
        raise Exception(f"The username {user.username} has more than 14 characters") 
    if len(user.username) < 1:
        raise Exception(f"The username is empty") 
    if not user.username.isalnum():
        raise Exception(f"The username should have only alphanumeric characters") 
    
    db.session.add(user)
    db.session.commit()
    return user

def put(body):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    user = User.query.get(body['id'])
    if user:
        user = User(**body)
        db.session.merge(user)
        db.session.flush()
        db.session.commit()
        return user
    raise NotFound('no such entity found with id=' + str(body['id']))

def delete(id):
    '''
    Delete entity by id
    :param id: the entity id
    :returns: the response
    '''
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'success': True}
    raise NotFound('no such entity found with id=' + str(id))


def check_if_exists(username):
    existing_users = db.session.query(User).filter(User.username==username).all()
    if len(existing_users) > 0:
        return True
    return False
        
def get_total_posts(user_id:int) -> int:
    qty = queries.get_total_posts(db.engine.raw_connection(), user_id=user_id)
    return qty