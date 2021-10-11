FROM python:3.10.0-slim-buster

LABEL maintainer="Himal Shakya"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN useradd -ms /bin/bash app_user
USER app_user
WORKDIR /home/app_user

COPY ./app /home/app_user
