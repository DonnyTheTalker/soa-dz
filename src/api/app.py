from flask import Flask

from auth_controller import AuthController
from user_controller import UserController

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    return AuthController.register()

@app.route('/update_profile', methods=['PATCH'])
def update_profile():
    return AuthController.update_profile()

@app.route('/login', methods=['POST'])
def authenticate():
    return AuthController.authenticate()

@app.route('/user', methods=['GET'])
def get_user():
    return UserController.get_user()

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')