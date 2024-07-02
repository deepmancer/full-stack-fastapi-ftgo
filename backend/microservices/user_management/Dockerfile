# Use the official Python image from the Docker Hub
FROM python:3.9.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Install grpcio-tools to generate pb2 files
RUN pip install grpcio-tools

# Generate pb2 files
RUN python -m grpc_tools.protoc -I./app/protos --python_out=./app/grpc_interface --grpc_python_out=./app/grpc_interface ./app/protos/user_service.proto

# Expose the gRPC port (will be dynamically allocated)
EXPOSE 50051

# Run the application
CMD ["python", "app/main.py"]
