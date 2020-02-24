FROM python:3.8

RUN pip install -U pip \
 && pip install pipenv

COPY . /opt/market/
WORKDIR /opt/market/

RUN pipenv install --system -d

#CMD ["python", "-m", "push"]