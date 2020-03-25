FROM python:3.8

RUN pip install -U pip \
 && pip install pipenv


ADD . /opt/websocket/
WORKDIR /opt/websocket/
RUN pipenv install --system -d