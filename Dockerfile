FROM python:3.10.0-slim-buster

LABEL maintainer="Himal Shakya"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt
RUN apt-get update && apt-get install -y gcc libc-dev python3-dev libpq-dev postgresql-client && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN useradd -ms /bin/bash app_user
USER app_user
WORKDIR /home/app_user

COPY ./app /home/app_user
