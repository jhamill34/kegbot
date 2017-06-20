#!bin/bash

if test -d node_modules;
then
  echo node_modules_exists ;
else
  cp -a /tmp/node_modules /app;
fi && npm install && npm start
