FROM gcr.io/tensorflow/tensorflow:latest-gpu
 
# Update OS
RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y upgrade
 
# Install Python
RUN apt-get install -y \
      python-dev \
      python-pip \
      build-essential \
      libssl-dev \
      libffi-dev \
      libxml2-dev \
      libxslt-dev \
      python-numpy \
      python-scipy \
      netbase \
      git \
      python-tk \
      nginx
 
# Add requirements.txt
ADD requirements.txt .
 
# Install app requirements
RUN pip install -r requirements.txt
 
# Create app directory
ADD . /webapp

# clone enhance repo
RUN cd /webapp && \
    git clone -b 3d https://github.com/EdwardJKim/enhance

# Set the default directory for our environment
ENV HOME /webapp
WORKDIR /webapp
 
# Expose port 8000, 8443 for uwsgi
EXPOSE 8000
EXPOSE 8443

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8443", "--certfile", "server.crt", "--keyfile", "server.key", "-k", "gevent", "--timeout", "120", "wsgi:app", "--log-file=-"]
