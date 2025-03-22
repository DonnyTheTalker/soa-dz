from flask import Flask
import os

from auth_controller import AuthController
from user_controller import UserController

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

if __name__ == '__main__':
    port = os.environ.get('API_SERVER_PORT', 5000)
    app.run(debug=True, port=port, host='0.0.0.0')