# docker build -t tink_parser_app .

FROM python:3.8.2-slim-buster

RUN apt-get update \
    && apt-get install -y libtk8.6

RUN pip install --upgrade pip \
    && pip install pylint

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
