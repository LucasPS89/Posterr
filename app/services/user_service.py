from models.User import User
from config import db
from werkzeug.exceptions import NotFound
from services.queries import queries

def get(user_id=None):
    '''
    Get all users or user by id
    :returns: User entity
    '''
    if user_id:
        user =  User.query.get(user_id)
        return user
    else:         
        return User.query.all()

def post(body):
    '''
    Create new user
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
    Update user by id
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
    Delete user by id
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