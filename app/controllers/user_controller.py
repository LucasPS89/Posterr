from flask import Blueprint, jsonify, request
import services.user_service as user_service
import services.post_service as post_service
from models.Post import Post
from models.User import User
from werkzeug.exceptions import HTTPException
import json

api_user = Blueprint('users', 'users')

@api_user.route('/users', methods=['GET'])
def api_get():
    
    ''' Get all users'''
    #teste = User.query.all()
    #teste = User.query.get(2)
    users = user_service.get()
    return jsonify([user.as_dict() for user in users])

@api_user.route('/users', methods=['POST'])
def api_post():
    ''' Create entity'''
    user = user_service.post(request.json)
    return jsonify(user.as_dict())

@api_user.route('/users/<string:id>', methods=['PUT', 'GET'])
def api_put(id):   
    if request.method == 'GET':
        #Get user by id
        user = user_service.get(id)
        return jsonify(user.as_dict())
    else:
        #Update by id
        body = request.json
        body['id'] = id
        res = user_service.put(body)
        return jsonify(res.as_dict()) if isinstance(res, User) else jsonify(res)
        
@api_user.route('/users/<string:id>/posts', methods=['GET'])
def api_get_posts(id):
    ''' Get user posts'''

    #Get page number from header
    page = 1
    if 'page' in request.headers:
        page = int(request.headers['page'])

    #Get Posts
    posts = post_service.get_homepage(id, None, None, 5, page)
    post_service
    return jsonify([post.as_dict() for post in posts])

@api_user.route('/users/<string:id>', methods=['DELETE'])
def api_delete(id):
    ''' Delete user by id'''
    res = user_service.delete(id)
    return jsonify(res)

@api_user.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON format for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        'success': False,
        "message": e.description
    })
    response.content_type = "application/json"
    return response

@api_user.errorhandler(Exception)
def unhandled_exception(e):
    error_message = str(e)
    # start with the correct headers and status code from the error
    response = {
        'success': False,
        "message": error_message
    }
    return response