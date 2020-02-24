FROM python:3.8

RUN pip install -U pip \
 && pip install pipenv

COPY . /opt/push/
WORKDIR /opt/push/

RUN pipenv install --system -d

#CMD ["python", "-m", "push"]