FROM python:3.11.7-slim

WORKDIR /opt

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

COPY ./requirements.txt /opt/requirements.txt

RUN pip install --no-cache-dir -r /opt/requirements.txt
