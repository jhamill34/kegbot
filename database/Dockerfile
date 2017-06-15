FROM postgres:9
MAINTAINER Joshua Rasmussen <xlr8runner@gmail.com>

COPY ./migrations/ /docer-entrypoint-initdb.d/

ENV POSTGRES_USER=docker
ENV POSTGRES_PASSWORD=mysecretpassword
ENV POSTGRES_DB=kegbot
