FROM tiangolo/uwsgi-nginx-flask:python3.6
LABEL maintainer="paulchandler3@mac.com"
LABEL version="v1.0.0"

COPY . /app

ENV LISTEN_PORT 5000
EXPOSE 5000