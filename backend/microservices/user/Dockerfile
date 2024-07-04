FROM python:3.9-slim

WORKDIR /user_service

# Set up Python behaviour
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv

# Switch on virtual environment
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the server port
EXPOSE 8000

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . /user_service/

ENV PYTHONPATH=/user_service/app/

CMD uvicorn user_service.app.main:app --reload --workers 4 --host 0.0.0.0 --port 8000
