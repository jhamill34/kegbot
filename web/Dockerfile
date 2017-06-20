# FROM resin/rpi-raspbian:latest
FROM debian:jessie
MAINTAINER Joshua Rasmussen <xlr8runner@gmail.com>

ENTRYPOINT []

RUN apt-get update && apt-get -y install curl \
	&& curl -sL https://deb.nodesource.com/setup_6.x | bash - \
	&& apt-get -y install nodejs

# Install node modules in a cache directory
COPY package.json /tmp/
WORKDIR /tmp
RUN npm install

# Move the cached modules to our app
COPY ./ /app
WORKDIR /app
RUN cp -a /tmp/node_modules/ /app/

ENV PORT=3000

CMD ["npm", "start"]

EXPOSE 3000
