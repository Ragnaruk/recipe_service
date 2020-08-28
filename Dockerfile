FROM python:3.7

ENV PYTHONPATH /recipe_service

WORKDIR /recipe_service
COPY ./requirements.txt /recipe_service/requirements.txt

RUN pip install -r /recipe_service/requirements.txt

COPY . /recipe_service