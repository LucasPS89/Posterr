from models.User import User
from models.Post import Post
from config import db
from services.queries import queries
from sqlalchemy import desc

def get_homepage(user_id=None, start_date=None, end_date=None, posts_per_page=10, page=1):
    my_query = Post.query
    if user_id:
        my_query = my_query.filter(Post.user_id == user_id)
    if start_date:
        my_query = my_query.filter(Post.datetime_creation >= start_date)
    if end_date:
        my_query = my_query.filter(Post.datetime_creation <= end_date)
    
    return my_query.order_by(desc(Post.datetime_creation)).paginate(page,posts_per_page,error_out=False).items

def post(body, repost_from_id=None, quote_from_id=None):
    '''
    Create entity with body
    :param body: request body
    :returns: the created entity
    '''
    post = Post(**body)

    #Add Reference Id if its a Repost or Quote
    if repost_from_id:
        post.repost_from_id = repost_from_id
    if quote_from_id:
        post.quote_from_id = quote_from_id

    #User cannot repost reposts, only original posts
    if repost_from_id:
        repost_from = Post.query.get(repost_from_id)
        if repost_from.repost_from_id:
            raise Exception(f"It's not allowed to repost a repost. You can only repost original posts or quotes") 

    #Use cannot quote others quotes, only reposts or posts
    if quote_from_id:
        quote_from = Post.query.get(quote_from_id)
        if quote_from.quote_from_id:
            raise Exception(f"It's not allowed to quote a quote. You can only quote reposts or original posts") 
    
    if len(post.text) > 777:
        raise Exception(f"The post text has more than 777 characters") 
    if len(post.text) < 1 and not repost_from_id :
        raise Exception(f"To post or quote, the text should have at least 1 character.")         
    if not post.user_id:
        raise Exception(f"The post has not user_id specified") 
    if not check_if_user_exists(post.user_id):
        raise Exception(f"The user_id specified does not exists") 
    if get_total_posts_today(post.user_id) > 5:
        raise Exception(f"This user has already posted 5 times today") 
    
    db.session.add(post)
    db.session.commit()
    return post

def get(post_id):
    '''
    Get post by id
    :returns: Post entity
    '''
    if not post_id:
        return
    
    post =  Post.query.get(post_id)
    return post

def get_total_posts_today(user_id:int) -> int:
    qty = queries.get_total_posts_today(db.engine.raw_connection(), user_id=user_id)
    return qty

def check_if_user_exists(user_id:int) -> bool:
    if not User.query.get(user_id):
        return False

    return True