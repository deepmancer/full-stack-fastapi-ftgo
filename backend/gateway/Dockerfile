# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /gateway

EXPOSE 8000

ENV ENVIRONMENT=dev

RUN apt-get update && apt-get install -y \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

COPY ./requirements.txt /gateway/requirements.txt

RUN pip install --no-cache-dir -r /gateway/requirements.txt

RUN pip install prometheus-fastapi-instrumentator

COPY ./ /gateway/

ENV PYTHONPATH=/gateway/src

EXPOSE 8000

CMD python /gateway/src/main.py
