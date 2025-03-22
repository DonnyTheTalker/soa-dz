import grpc
import os
from flask import jsonify, request

from proto.auth_pb2 import UserRequest
from proto.auth_pb2_grpc import AuthServiceStub


class UserController:
    @staticmethod
    def grpc_channel():
        host = os.environ.get('USER_GRPC_SERVER_HOST', 'user')
        port = os.environ.get('USER_GRPC_SERVER_PORT', 50051)
        return grpc.insecure_channel(f'{host}:{port}')

    @staticmethod
    def get_user():
        username = request.args.get('username', None)

        if not username:
            return jsonify(success=False, message="Username is required"), 400

        with UserController.grpc_channel() as channel:
            stub = AuthServiceStub(channel)
            response = stub.GetUserDetails(UserRequest(username=username))
            if response.found:
                return jsonify(
                    success=True,
                    first_name=response.first_name,
                    last_name=response.last_name,
                    birth_date=response.birth_date,
                    email=response.email,
                    phone_number=response.phone_number,
                    username=response.username
                ), 200
            else:
                return jsonify(success=False, message="User not found"), 404
