from flask import Blueprint, jsonify, request
import services.user_service as user_service
import services.post_service as post_service
from werkzeug.exceptions import HTTPException
import json
from services.util import validate_date

api_post = Blueprint('post', 'post')

#Homepage
@api_post.route('/homepage', methods=['GET'])
def api_get_homepage():
    ''' Get Homepage. All and Only Mine'''

    #Get user from header, but it should be from the session
    user_id = None
    if 'user_id' in request.headers:
        user_id = int(request.headers['user_id'])    

    #Get page number from header
    page = 1
    if 'page' in request.headers:
        page = int(request.headers['page'])

    #Start Date Filter
    start_date = None
    if 'start_date' in request.headers:
        start_date = request.headers['start_date']
        validate_date(start_date)

    #End Date Filter
    end_date = None
    if 'end_date' in request.headers:
        end_date = request.headers['end_date']
        validate_date(end_date)

    #Load Posts 
    posts = post_service.get_homepage(user_id, start_date, end_date, 10, page)
    return jsonify([post.as_dict() for post in posts])

#Create POST
@api_post.route('/posts', methods=['POST'])
def api_create_post():
    ''' Create a new POST from scratch'''
    post = post_service.post(request.json)
    return jsonify(post.as_dict())

#Get Post by Id
@api_post.route('/posts/<string:id>', methods=['GET'])
def api_get_post(id):   
    #Get post by id
    post = post_service.get(id)
    return jsonify(post.as_dict())

#Repost
@api_post.route('/posts/<string:id>/repost', methods=['POST'])
def api_repost(id):   
    ''' Repost a post'''
    post = post_service.post(request.json, id, None)
    post = post_service.get(post.id)
    return jsonify(post.as_dict())

#Quote
@api_post.route('/posts/<string:id>/quote', methods=['POST'])
def api_quote(id):   
    ''' Repost a post'''
    post = post_service.post(request.json, None, id)
    post = post_service.get(post.id)
    return jsonify(post.as_dict())

#Error Handling
@api_post.errorhandler(HTTPException)
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

@api_post.errorhandler(Exception)
def unhandled_exception(e):
    error_message = str(e)
    # start with the correct headers and status code from the error
    response = {
        'success': False,
        "message": error_message
    }
    return response