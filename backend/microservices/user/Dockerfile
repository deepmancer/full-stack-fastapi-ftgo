# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV ENVIRONMENT=dev

# Set the server port
EXPOSE 5020

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip

# Copy requirements.txt before other files to leverage Docker cache
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the application code to the container
COPY . /user_service

# Set the working directory
WORKDIR /user_service

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/user_service/src

# Copy the Alembic configuration file
COPY alembic.ini /user_service/alembic.ini

# Copy the entry point script
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Command to run the entry point script
ENTRYPOINT ["/entrypoint.sh"]
