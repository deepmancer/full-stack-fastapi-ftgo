# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the server port
EXPOSE 5020
# # Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

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
ENV PYTHONPATH=/user_service/app

# Command to run the application
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5020"]
