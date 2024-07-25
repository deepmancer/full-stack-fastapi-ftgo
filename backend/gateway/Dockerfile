# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV ENVIRONMENT=dev
EXPOSE 8000

# Upgrade pip and install Python dependencies
#RUN apt-get update
#RUN apt-get install -y git
RUN apt-get update && apt-get install -y git ca-certificates
# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt before other files to leverage Docker cache
COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt --upgrade

# Copy the application code to the container
COPY . /gateway

# Expose the port to the outside world
# Set the working directory
WORKDIR /gateway

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/gateway/src

# Run Alembic migrations and start the application
CMD python src/main.py
