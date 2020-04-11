# docker build -t tink_parser_app .

FROM python:3.6.10-slim-buster

RUN pip install --upgrade pip \
    && pip install pylint