FROM python:3.8

RUN pip install -U pip \
 && pip install pipenv

COPY . /opt/auth/
WORKDIR /opt/auth/

RUN pipenv install --system -d