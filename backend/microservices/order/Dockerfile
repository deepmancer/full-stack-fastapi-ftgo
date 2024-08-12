# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV ENVIRONMENT=dev

# Upgrade pip and install Python dependencies
#RUN apt-get update
#RUN apt-get install -y git
RUN apt-get update && \
    apt-get install -y git ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 
# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt before other files to leverage Docker cache
COPY ./requirements.txt /tmp/requirements.txt


RUN pip install -r /tmp/requirements.txt --no-cache-dir --force-reinstall
RUN pip install --upgrade --no-deps git+https://github.com/deepmancer/aredis-client.git
# Copy the application code to the container
COPY . /order

# Set the working directory
WORKDIR /order

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/order/src

# RUN python -m pytest -v
# Copy the Alembic configuration file
# COPY alembic.ini /order/alembic.ini

# Run Alembic migrations and start the application
CMD python -u src/main.py
