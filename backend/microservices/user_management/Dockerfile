# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Install the dependencies
RUN poetry install

# Copy the content of the local src directory to the working directory
COPY . .

# Install redis-py
RUN poetry add redis

# Make ports 50051 and 8000 available to the world outside this container
EXPOSE 50051
EXPOSE 8000

# Define the command to run the application
CMD ["poetry", "run", "python", "app/main.py"]
