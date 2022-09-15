from config import app
from controllers.user_controller import api_user
from controllers.post_controller import api_post

# register the api
app.register_blueprint(api_user)
app.register_blueprint(api_post)

if __name__ == '__main__':
    ''' run application '''
    app.run(host='0.0.0.0', port=5000)
