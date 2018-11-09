FROM ubuntu:18.04
MAINTAINER Robert Piskule <piskule@synopsys.com>
RUN apt-get update && \
    apt-get install -y python python-pip python-dev build-essential emacs libgnutls28-dev libcurl4-gnutls-dev
RUN pip install --upgrade pip
RUN pip install --upgrade kubernetes openshift pycurl pyyaml

#DELETE ME
RUN apt-get install -y curl

ADD src/opt/ /

EXPOSE 8080