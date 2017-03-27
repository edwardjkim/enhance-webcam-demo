#!/bin/sh
sudo docker build -t edwardjkim/flask .
sudo docker rm -f flask
sudo nvidia-docker run -d -p 443:8443 \
  --name flask \
  edwardjkim/flask
