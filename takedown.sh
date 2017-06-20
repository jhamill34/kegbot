#!/bin/bash 

docker stop kegbot-container
docker stop kegbot-db-container
docker stop kegbot-api-container 
docker network rm kegbot-network
