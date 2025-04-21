from concurrent import futures
import grpc
from proto import posts_pb2, posts_pb2_grpc

from kafka_producer import PostsEventProducer
from db import SessionLocal, engine
from models import Base
import crud
import os

Base.metadata.create_all(bind=engine)


class PostService(posts_pb2_grpc.PostServiceServicer):
    def __init__(self):
        self.producer = PostsEventProducer()

    def CreatePost(self, request, context):
        with SessionLocal() as db:
            post = crud.create_post(
                db, request.title, request.description, request.creator_id, request.is_private, request.tags
            )
            return posts_pb2.PostResponse(success=True, message="Post created", post=self._post_to_response(post))

    def DeletePost(self, request, context):
        with SessionLocal() as db:
            result = crud.delete_post(db, request.id, request.creator_id)
            message = "Post deleted" if result else "Post not found or access denied"
            return posts_pb2.PostResponse(success=result, message=message)

    def UpdatePost(self, request, context):
        with SessionLocal() as db:
            post = crud.update_post(
                db,
                request.id,
                request.creator_id,
                request.title if request.title else None,
                request.description if request.description else None,
                request.is_private if request.is_private else None,
                request.tags if request.tags else None,
            )
            if post:
                return posts_pb2.PostResponse(success=True, message="Post updated", post=self._post_to_response(post))
            else:
                return posts_pb2.PostResponse(success=False, message="Post not found or access denied")

    def GetPost(self, request, context):
        with SessionLocal() as db:
            post = crud.get_post(db, request.id, request.creator_id)
            if post:
                self.producer.send_view_event(
                    request.creator_id,
                    "post",
                    request.id,
                )
                return posts_pb2.PostResponse(success=True, message="Post found", post=self._post_to_response(post))
            else:
                return posts_pb2.PostResponse(success=False, message="Post not found or access denied")

    def ListPosts(self, request, context):
        with SessionLocal() as db:
            posts = crud.list_posts(db, request.page_number, request.page_size, request.creator_id, request.author_id)

            for post in posts:
                self.producer.send_view_event(
                    request.creator_id,
                    "post",
                    post.id,
                )

            response_posts = [self._post_to_response(post) for post in posts]
            return posts_pb2.ListPostsResponse(success=True, posts=response_posts)

    def LikePost(self, request, context):
        with SessionLocal() as db:
            if not crud.get_post(db, request.post_id, request.creator_id):
                return posts_pb2.LikePostResponse(success=False, message="Post not found or access denied")
            if crud.get_like(db, request.post_id, request.creator_id):
                return posts_pb2.LikePostResponse(success=False, message="Post already liked")
            crud.like_post(db, request.post_id, request.creator_id)

            self.producer.send_like_event(
                request.creator_id,
                "post",
                request.post_id,
            )

            return posts_pb2.LikePostResponse(success=True, message="Post liked")

    def UnlikePost(self, request, context):
        with SessionLocal() as db:
            if not crud.get_post(db, request.post_id, request.creator_id):
                return posts_pb2.LikePostResponse(success=False, message="Post not found or access denied")
            if not crud.get_like(db, request.post_id, request.creator_id):
                return posts_pb2.LikePostResponse(success=False, message="Post not liked")
            crud.unlike_post(db, request.post_id, request.creator_id)

            self.producer.send_unlike_event(
                request.creator_id,
                "post",
                request.post_id,
            )

            return posts_pb2.LikePostResponse(success=True, message="Post unliked")

    def LeaveComment(self, request, context):
        with SessionLocal() as db:
            if not crud.get_post(db, request.post_id, request.creator_id):
                return posts_pb2.LeaveCommentResponse(success=False, message="Post not found or access denied")
            comment = crud.leave_comment(db, request.post_id, request.creator_id, request.text)

            self.producer.send_comment_event(
                request.creator_id,
                "post",
                request.post_id,
            )

            return posts_pb2.LeaveCommentResponse(
                success=True, message="Comment left", comment=self._comment_to_response(comment)
            )

    def ListComments(self, request, context):
        with SessionLocal() as db:
            comments = crud.list_comments(db, request.post_id, request.page_number, request.page_size)
            response_comments = [self._comment_to_response(comment) for comment in comments]
            return posts_pb2.ListCommentsResponse(success=True, comments=response_comments)

    def _comment_to_response(self, comment):
        return posts_pb2.Comment(
            id=comment.id,
            post_id=comment.post_id,
            creator_id=comment.creator_id,
            text=comment.comment,
            created_at=str(comment.created_at),
        )

    def _post_to_response(self, post):
        return posts_pb2.Post(
            id=post.id,
            title=post.title,
            description=post.description,
            creator_id=post.creator_id,
            created_at=str(post.created_at),
            updated_at=str(post.updated_at),
            is_private=post.is_private,
            tags=post.tags,
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    posts_pb2_grpc.add_PostServiceServicer_to_server(PostService(), server)
    port = os.environ.get('POSTS_SERVER_PORT', 50052)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
