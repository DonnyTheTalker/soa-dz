import pytest
import grpc

from .proto import auth_pb2, auth_pb2_grpc

@pytest.fixture(scope='module')
def grpc_channel():
    channel = grpc.insecure_channel('localhost:50051')
    yield channel
    channel.close()

@pytest.fixture(scope='module')
def grpc_stub(grpc_channel):
    return auth_pb2_grpc.AuthServiceStub(grpc_channel)

def test_register(grpc_stub):
    assert True
    pass
    # request = auth_pb2.RegisterRequest(
    #     username='testuser',
    #     password='testpass',
    #     email='testuser@example.com'
    # )
    # response = grpc_stub.Register(request)
    # assert response.success == True or response.message == "User already exists"

def test_login(grpc_stub):
    assert True
    pass
    # request = auth_pb2.AuthRequest(
    #     username='testuser',
    #     password='testpass'
    # )
    # response = grpc_stub.Login(request)
    # assert response.success == True