import grpc
import re
from datetime import datetime
from flask import request, jsonify

from proto.auth_pb2 import RegisterRequest, AuthenticateRequest, ProfileUpdateRequest
from proto.auth_pb2_grpc import AuthServiceStub


class AuthController:
    @staticmethod
    def grpc_channel():
        return grpc.insecure_channel('user:50051')

    @staticmethod
    def register():
        data = request.get_json()

        required_fields = ['email', 'username', 'password']
        if not AuthController.check_required_fields(data, required_fields):
            return jsonify(success=False, message="Missing fields"), 400

        valid, message = AuthController.validate_registration_data(data)
        if not valid:
            return jsonify(success=False, message=message), 400
        
        with AuthController.grpc_channel() as channel:
            stub = AuthServiceStub(channel)
            response = stub.RegisterUser(RegisterRequest(
                email=data['email'],
                username=data['username'],
                password=data['password']
            ))
            return jsonify(success=response.success, message=response.message), 200 if response.success else 400
        
    @staticmethod
    def update_profile():
        data = request.get_json()

        required_fields = ['username']
        if not AuthController.check_required_fields(data, required_fields):
            return jsonify(success=False, message="Missing fields"), 400
        
        valid, message = AuthController.validate_registration_data(data)
        if not valid:
            return jsonify(success=False, message=message), 400

        with AuthController.grpc_channel() as channel:
            stub = AuthServiceStub(channel)
            response = stub.UpdateUserProfile(ProfileUpdateRequest(
                username=data['username'],
                first_name=data.get('first_name', None),
                last_name=data.get('last_name', None),
                birth_date=data.get('birth_date', None),
                phone_number=data.get('phone_number', None)
            ))
            return jsonify({"success": response.success, "message": response.message})

    @staticmethod
    def authenticate():
        data = request.get_json()

        required_fields = ['username', 'password']
        if not AuthController.check_required_fields(data, required_fields):
            return jsonify(success=False, message="Missing fields"), 400

        with AuthController.grpc_channel() as channel:
            stub = AuthServiceStub(channel)
            response = stub.AuthenticateUser(AuthenticateRequest(
                username=data['username'],
                password=data['password']
            ))
            return jsonify(success=response.success, message=response.message), 200 if response.success else 401
    
    @staticmethod
    def validate_registration_data(data):
        if 'birth_date' in data and not AuthController.is_valid_birth_date(data['birth_date']):
            return False, "Invalid or too old birth date"

        if 'email' in data and not AuthController.is_valid_email(data['email']):
            return False, "Invalid email format"

        if 'phone_number' in data and not AuthController.is_valid_phone_number(data['phone_number']):
            return False, "Invalid phone number format"

        if 'password' in data and not AuthController.is_valid_password(data['password']):
            return False, "Password must be at least 8 characters long, contain a number and an uppercase letter"

        return True, ""
    
    @staticmethod
    def check_required_fields(data, required_fields):
        return all(field in data for field in required_fields)
    
    @staticmethod
    def is_valid_birth_date(birth_date_str):
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
            return birth_date >= datetime(1970, 1, 1)
        except ValueError:
            return False

    @staticmethod
    def is_valid_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def is_valid_phone_number(phone_number):
        phone_regex = r'^\+?1?\d{9,15}$'
        return re.match(phone_regex, phone_number) is not None

    @staticmethod
    def is_valid_password(password):
        if len(password) < 8:
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[A-Z]', password):
            return False
        return True