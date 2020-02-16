FROM vaultvulp/pipenv-ubuntu:3.8

COPY ./ /opt/push
WORKDIR /opt/push

RUN pipenv install -d

CMD ["python", "-m", "push"]