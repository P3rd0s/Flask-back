FROM python:3.9.16-slim-bullseye


WORKDIR /usr/src/app/FlaskBack

COPY requirements.txt /usr/src/app/FlaskBack
RUN apt-get update && \
    apt-get -y install libpq-dev gcc && \
    pip install -r /usr/src/app/FlaskBack/requirements.txt
COPY . /usr/src/app/FlaskBack

ENV REDIS=REDIS
ENV POSTGRES=POSTGRES
ENV POSTGRES_DB=articlesdb
ENV POSTGRES_TABLE=articles
ENV POSTGRES_USER=iocsfinder
ENV POSTGRES_PASSWORD=strongHeavyPassword4thisdb

EXPOSE 5000
CMD ["python3", "app.py"]