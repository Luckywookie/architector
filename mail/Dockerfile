FROM python:3.8

RUN pip install -U pip \
 && pip install pipenv


ADD . /opt/app/
WORKDIR /opt/app/
RUN pipenv install --system -d

#WORKDIR /opt/

#CMD ["python", "-m", "app"]