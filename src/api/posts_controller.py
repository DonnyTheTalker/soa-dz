import grpc
import re
import os

from flask import request, jsonify

from proto import posts_pb2, posts_pb2_grpc
from auth_controller import AuthController
from google.protobuf.json_format import MessageToDict


class PostsController:
    @staticmethod
    def grpc_channel():
        host = os.environ.get('POSTS_GRPC_SERVER_HOST', 'posts')
        port = os.environ.get('POSTS_GRPC_SERVER_PORT', 50052)
        return grpc.insecure_channel(f'{host}:{port}')

    @staticmethod
    def create_post():
        data = request.get_json()

        with PostsController.grpc_channel() as channel:
            stub = posts_pb2_grpc.PostServiceStub(channel)
            grpc_request = posts_pb2.CreatePostRequest(
                title=data['title'],
                description=data['description'],
                creator_id=data['username'],
                is_private=data.get('is_private', False),
                tags=data.get('tags', []),
            )
            response = stub.CreatePost(grpc_request)
            return jsonify(
                {"success": response.success, "message": response.message, "post": MessageToDict(response.post)}
            ), (200 if response.success else 400)

    @staticmethod
    def delete_post():
        data = request.get_json()

        required_fields = ['id', 'username']
        if not AuthController.check_required_fields(data, required_fields):
            return jsonify(success=False, message="Missing fields"), 400

        with PostsController.grpc_channel() as channel:
            stub = posts_pb2_grpc.PostServiceStub(channel)
            grpc_request = posts_pb2.DeletePostRequest(id=data['id'], creator_id=data['username'])
            response = stub.DeletePost(grpc_request)
            return jsonify({"success": response.success, "message": response.message}), 200 if response.success else 400

    @staticmethod
    def update_post():
        data = request.get_json()

        required_fields = ['id', 'username']
        if not AuthController.check_required_fields(data, required_fields):
            return jsonify(success=False, message="Missing fields"), 400

        with PostsController.grpc_channel() as channel:
            stub = posts_pb2_grpc.PostServiceStub(channel)
            grpc_request = posts_pb2.UpdatePostRequest(
                id=data['id'],
                title=data.get('title', None),
                description=data.get('description', None),
                creator_id=data['username'],
                is_private=data.get('is_private', None),
                tags=data.get('tags', None),
            )
            response = stub.UpdatePost(grpc_request)
            return jsonify(
                {"success": response.success, "message": response.message, "post": MessageToDict(response.post)}
            ), (200 if response.success else 400)

    @staticmethod
    def get_post():
        data = request.get_json()

        required_fields = ['id', 'username']
        if not AuthController.check_required_fields(data, required_fields):
            return jsonify(success=False, message="Missing fields"), 400

        with PostsController.grpc_channel() as channel:
            stub = posts_pb2_grpc.PostServiceStub(channel)
            grpc_request = posts_pb2.GetPostRequest(id=data['id'], creator_id=data['username'])
            response = stub.GetPost(grpc_request)
            return jsonify(
                {"success": response.success, "message": response.message, "post": MessageToDict(response.post)}
            ), (200 if response.success else 400)

    @staticmethod
    def list_posts():
        data = request.get_json()

        required_fields = ['username', 'author']
        if not AuthController.check_required_fields(data, required_fields):
            return jsonify(success=False, message="Missing fields"), 400

        with PostsController.grpc_channel() as channel:
            stub = posts_pb2_grpc.PostServiceStub(channel)
            page_number = data.get('page_number', 0)
            page_size = data.get('page_size', 10)
            grpc_request = posts_pb2.ListPostsRequest(
                creator_id=data['username'], page_number=page_number, page_size=page_size,
                author_id=data['author']
            )
            response = stub.ListPosts(grpc_request)
            return jsonify(
                {
                    "success": response.success,
                    "message": response.message,
                    "posts": [MessageToDict(post) for post in response.posts],
                }
            ), (200 if response.success else 400)
