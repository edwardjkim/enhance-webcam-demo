FROM ubuntu:14.04
 
# Update OS
RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y upgrade
 
# Install Python
RUN apt-get install -y python-dev python-pip build-essential libssl-dev libffi-dev libxml2-dev libxslt-dev
 
# Add requirements.txt
ADD requirements.txt .
 
# Install uwsgi Python web server
RUN pip install --upgrade six
RUN pip install uwsgi
# Install app requirements
RUN pip install -r requirements.txt
 
# Create app directory
ADD . /webapp
 
# Set the default directory for our environment
ENV HOME /webapp
WORKDIR /webapp
 
# Expose port 8000, 8443 for uwsgi
EXPOSE 8000
EXPOSE 8443

ENTRYPOINT ["uwsgi", "--https", "0.0.0.0:8443,server.crt,server.key", "--module", "app:app", "--processes", "1", "--threads", "8"]
