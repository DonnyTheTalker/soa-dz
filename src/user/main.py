from concurrent import futures
import grpc

from proto import auth_pb2, auth_pb2_grpc
from db import SessionLocal, engine
from models import Base
from crud import create_user, authenticate_user, get_user, update_user_profile

Base.metadata.create_all(bind=engine)

class AuthServicer(auth_pb2_grpc.AuthServiceServicer):
    def RegisterUser(self, request, context):
        with SessionLocal() as db:
            user = create_user(
                db,
                username=request.username,
                password=request.password,
                email=request.email
            )
            if user is not None:
                return auth_pb2.RegisterResponse(success=True, message="User created")
            return auth_pb2.RegisterResponse(success=False, message="User already exists")

    def AuthenticateUser(self, request, context):
        with SessionLocal() as db:
            valid = authenticate_user(db, request.username, request.password)
            return auth_pb2.AuthenticateResponse(success=valid, message="Auth succeeded" if valid else "Invalid credentials")

    def GetUserDetails(self, request, context):
        with SessionLocal() as db:
            user = get_user(db, request.username)
            if user:
                return auth_pb2.UserResponse(
                    found=True,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    birth_date=str(user.birth_date),
                    email=user.email,
                    phone_number=user.phone_number,
                )
            return auth_pb2.UserResponse(found=False)
        
    def UpdateUserProfile(self, request, context):
        with SessionLocal() as db:
            user = update_user_profile(
                db,
                username=request.username,
                first_name=(request.first_name if request.first_name else None),
                last_name=(request.last_name if request.last_name else None),
                birth_date=(request.birth_date if request.birth_date else None),
                phone_number=(request.phone_number if request.phone_number else None)
            )
            if user:
                return auth_pb2.UpdateResponse(success=True, message="User profile updated")
            return auth_pb2.UpdateResponse(success=False, message="User not found or error occurred")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
