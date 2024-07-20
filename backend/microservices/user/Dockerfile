# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV ENVIRONMENT=dev

# Set the server port
EXPOSE 5020

# Upgrade pip and install Python dependencies
RUN apt-get update && apt-get install -y git

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt before other files to leverage Docker cache
COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt
RUN pip install --upgrade git+https://github.com/alirezaheidari-cs/ftgo_utils.git
RUN pip install --force-reinstall --no-cache-dir --upgrade git+https://github.com/alirezaheidari-cs/rabbitmq_rpc.git

# Copy the application code to the container
COPY . /user

# Set the working directory
WORKDIR /user

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/user/src

# Copy the Alembic configuration file
COPY alembic.ini /user/alembic.ini

# Run Alembic migrations and start the application
CMD alembic upgrade head && python src/main.py
