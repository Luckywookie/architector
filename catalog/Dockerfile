FROM python:3.8

RUN pip install -U pip \
 && pip install pipenv

COPY . /opt/catalog/
WORKDIR /opt/catalog/

RUN pipenv install --system -d