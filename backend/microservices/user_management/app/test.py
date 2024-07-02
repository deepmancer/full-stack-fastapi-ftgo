import grpc
from grpc_interface import user_service_pb2, user_service_pb2_grpc

def run():
    # Connect to the gRPC server
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_service_pb2_grpc.UserServiceStub(channel)

    # Test Register method
    print("Testing Register method...")
    register_request = user_service_pb2.RegisterRequest(
        first_name="John",
        last_name="Doe",
        phone_number="1234567890",
        password="password"
    )
    register_response = stub.Register(register_request)
    print("Register response received:", register_response.auth_code)

    # Test AuthenticatePhoneNumber method
    print("Testing AuthenticatePhoneNumber method...")
    authenticate_request = user_service_pb2.AuthenticatePhoneNumberRequest(
        phone_number="1234567890",
        auth_code=register_response.auth_code
    )
    authenticate_response = stub.AuthenticatePhoneNumber(authenticate_request)
    print("AuthenticatePhoneNumber response received:", authenticate_response.success)

if __name__ == '__main__':
    run()
