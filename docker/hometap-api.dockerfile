FROM python:slim

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt