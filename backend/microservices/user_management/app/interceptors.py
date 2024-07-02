from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import NotFound
from grpc_interceptor import ExceptionToStatusInterceptor

class ErrorLogger(ServerInterceptor):
    def intercept(self, method, request, context, method_name):
        try:
            return method(request, context)
        except Exception as e:
            self.log_error(e)
            raise

    def log_error(self, e: Exception) -> None:
        # Log the error here (you can customize this to log to a file, a monitoring system, etc.)
        print(f"Error occurred: {e}")

def get_interceptors():
    return [
        ErrorLogger(),
        ExceptionToStatusInterceptor()
    ]
