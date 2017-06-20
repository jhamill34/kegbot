#!/bin/bash 

docker network create -d bridge --subnet 172.20.0.0/16 --gateway 172.20.0.1  kegbot-network

docker run --network kegbot-network --rm -d -v /home/pi/kegbot/db/data:/var/lib/postgresql/data --name kegbot-db-container kegbot-db
docker run --network kegbot-network --rm -d --privileged --name kegbot-container kegbot-base
docker run --network kegbot-network --rm -d -p 3000:3000 --name kegbot-api-container kegbot-api
