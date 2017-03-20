#!/bin/sh
sudo docker build -t edwardjkim/flask .
sudo docker rm -f flask
sudo docker run -d -p 8443:8443 \
  -v /home/paperspace/shared/enhance/generated:/webapp/upsampled_images \
  -v /home/paperspace/shared/enhance/test:/webapp/original_images \
  --name flask \
  edwardjkim/flask

