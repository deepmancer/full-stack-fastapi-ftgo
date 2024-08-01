# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV ENVIRONMENT=dev

# Upgrade pip and install Python dependencies
#RUN apt-get update
#RUN apt-get install -y git
RUN apt-get update && apt-get install -y git ca-certificates

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt before other files to leverage Docker cache
COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt --force-reinstall --upgrade

# Copy the application code to the container
COPY . /restaurant

# Set the working directory
WORKDIR /restaurant

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/restaurant/src

# Copy the Alembic configuration file
COPY alembic.ini /restaurant/alembic.ini

# Run Alembic migrations and start the application
CMD alembic upgrade head && python src/main.py
