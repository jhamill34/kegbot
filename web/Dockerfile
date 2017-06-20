FROM resin/rpi-raspbian:latest
MAINTAINER Joshua Rasmussen <xlr8runner@gmail.com>

ENTRYPOINT []

RUN apt-get update && apt-get -y install curl \
	&& curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash - \
	&& apt-get -y install nodejs


WORKDIR /app

COPY ./ /app

RUN npm install

CMD ["npm", "start"]
