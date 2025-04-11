from flask import Flask
import os

from auth_controller import AuthController
from user_controller import UserController
from posts_controller import PostsController

app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register():
    return AuthController.register()


@app.route('/update_profile', methods=['PATCH'])
def update_profile():
    auth_response, status_code = AuthController.authenticate()
    if status_code != 200:
        return auth_response, status_code
    return AuthController.update_profile()


@app.route('/login', methods=['POST'])
def authenticate():
    return AuthController.authenticate()


@app.route('/user', methods=['GET'])
def get_user():
    return UserController.get_user()


@app.route('/create_post', methods=['POST'])
def create_post():
    auth_response, status_code = AuthController.authenticate()
    if status_code != 200:
        return auth_response, status_code
    return PostsController.create_post()


@app.route('/delete_post', methods=['DELETE'])
def delete_post():
    auth_response, status_code = AuthController.authenticate()
    if status_code != 200:
        return auth_response, status_code
    return PostsController.delete_post()


@app.route('/update_post', methods=['PATCH'])
def update_post():
    auth_response, status_code = AuthController.authenticate()
    if status_code != 200:
        return auth_response, status_code
    return PostsController.update_post()


@app.route('/get_post', methods=['GET'])
def get_post():
    auth_response, status_code = AuthController.authenticate()
    if status_code != 200:
        return auth_response, status_code
    return PostsController.get_post()


@app.route('/list_posts', methods=['GET'])
def list_posts():
    auth_response, status_code = AuthController.authenticate()
    if status_code != 200:
        return auth_response, status_code
    return PostsController.list_posts()


@app.route('/like_post', methods=['POST'])
def like_post():
    auth_response, status_code = AuthController.authenticate()
    if status_code != 200:
        return auth_response, status_code
    return PostsController.like_post()


@app.route('/unlike_post', methods=['POST'])
def unlike_post():
    auth_response, status_code = AuthController.authenticate()
    if status_code != 200:
        return auth_response, status_code
    return PostsController.unlike_post()


@app.route('/comment_post', methods=['POST'])
def comment_post():
    auth_response, status_code = AuthController.authenticate()
    if status_code != 200:
        return auth_response, status_code
    return PostsController.comment_post()


@app.route('/list_comments', methods=['GET'])
def list_comments():
    auth_response, status_code = AuthController.authenticate()
    if status_code != 200:
        return auth_response, status_code
    return PostsController.list_comments()


if __name__ == '__main__':
    port = os.environ.get('API_SERVER_PORT', 5000)
    app.run(debug=True, port=port, host='0.0.0.0')
